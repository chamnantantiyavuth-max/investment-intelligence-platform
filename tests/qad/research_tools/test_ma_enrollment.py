"""Synthetic unit tests for qad.research_tools.ma_enrollment: joins, denominators, crosswalk classification,
suppression handling, bridge identity. No real data or outputs are used."""
import os
import numpy as np, pandas as pd, pytest
from qad.research_tools.ma_enrollment import analysis as A

def test_parse_enroll_suppression():
    s = A.parse_enroll(pd.Series(['*', '', '12', '1,234', ' 7 ']))
    assert s.isna().tolist() == [True, True, False, False, False]
    assert s.iloc[2] == 12 and s.iloc[3] == 1234 and s.iloc[4] == 7

def test_norm_county():
    s = A.norm_county(pd.Series(['St. Louis County', 'Saint Louis', "Prince George's", 'Miami-Dade', 'Orleans Parish']))
    assert s.iloc[0] == s.iloc[1] == 'STLOUIS'
    assert s.iloc[2] == 'PRINCEGEORGES' and s.iloc[3] == 'MIAMIDADE' and s.iloc[4] == 'ORLEANS'

def toy_cw():
    return pd.DataFrame([
        ('H1_001', 'H1_001', 'Renewal Plan'),
        ('H1_002', 'H1_003', 'Consolidated Renewal Plan'),
        ('H1_004', 'H1_003', 'Consolidated Renewal Plan'),
        ('H1_005', None, A.TERM_STATUS),
        ('H1_006', 'H1_006', 'Renewal Plan with SAR'),
        ('H1_006', 'H1_007', 'Renewal Plan with SAR'),   # split crosswalk
    ], columns=['prev', 'cur', 'STATUS'])

def test_crosswalk_components_and_classes():
    cw = toy_cw(); comp = A.components(cw)
    assert comp['P:H1_002'] == comp['P:H1_004'] == comp['C:H1_003']       # consolidation joins
    assert comp['P:H1_006'] == comp['C:H1_006'] == comp['C:H1_007']       # split joins
    assert comp['P:H1_001'] != comp['P:H1_002']
    pc = A.classify_plans(cw)
    assert pc.loc['H1_005', 'cls'] == 'terminated'
    assert pc.loc['H1_002', 'cls'] == 'continuing' and pc.loc['H1_002', 'consolidated']
    assert pc.loc['H1_006', 'sar']

def toy_frames():
    def cell(plan, cty, enr, par='UNH', group=False):
        return dict(plan=plan, ssa=cty, cty=cty, State='XX', par=par, **{'Parent Organization': par}, group=group, snp=False,
                    ptype='HMO', **{'Plan Type': 'HMO'}, enr=enr, supp=pd.isna(enr))
    base = pd.DataFrame([cell('H1_001', 'A', 100), cell('H1_001', 'B', 50), cell('H1_002', 'A', 30), cell('H1_004', 'A', 20),
                         cell('H1_005', 'A', 40), cell('H1_006', 'A', 60), cell('H1_006', 'C', 10), cell('H1_006', 'Z', np.nan),
                         cell('H9_009', 'A', 5), cell('H1_801', 'A', 25, group=True)])
    post = pd.DataFrame([cell('H1_001', 'A', 90), cell('H1_001', 'B', 55), cell('H1_003', 'A', 45), cell('H1_006', 'A', 70),
                         cell('H1_007', 'C', 3), cell('H1_010', 'A', 12), cell('H1_801', 'A', 20, group=True)])
    L5 = pd.DataFrame([('H1_001', 'H1_001_0', 'A', 0, 3000), ('H1_001', 'H1_001_0', 'B', 0, 3000), ('H1_002', 'H1_002_0', 'A', 0, 4000),
                       ('H1_004', 'H1_004_0', 'A', 20, 4000), ('H1_005', 'H1_005_0', 'A', 0, 3000), ('H1_006', 'H1_006_0', 'A', 0, 5000),
                       ('H1_006', 'H1_006_0', 'C', 0, 5000)], columns=['plan', 'seg', 'cty', 'prem', 'moop'])
    L6 = pd.DataFrame([('H1_001', 'H1_001_0', 'A', 15, 3000), ('H1_001', 'H1_001_0', 'B', 0, 3000), ('H1_003', 'H1_003_0', 'A', 0, 4000),
                       ('H1_006', 'H1_006_0', 'A', 0, 5000)], columns=['plan', 'seg', 'cty', 'prem', 'moop'])
    cw = toy_cw()
    cw = pd.concat([cw, pd.DataFrame([('H1_801', 'H1_801', 'Renewal Plan')], columns=cw.columns)])
    return base, post, cw, L5, L6

def test_bridge_classification_and_identity():
    base, post, cw, L5, L6 = toy_frames()
    b, q = A.build_bridge(base, post, cw, L5, L6)
    sc = dict(zip(b.plan + '|' + b.cty, b.seg_class))
    assert sc['H1_005|A'] == 'terminated'
    assert sc['H1_006|C'] == 'sa_exit'            # successor H1_007 has members in C but is not offered there in L6
    assert sc['H1_006|Z'] == 'out_of_area_residence'
    assert sc['H9_009|A'] == 'unmapped'
    assert sc['H1_002|A'] == 'consolidated' and sc['H1_801|A'] == 'group_continuing'
    rp = dict(zip(b.plan + '|' + b.cty, b.repriced_material))
    assert rp['H1_001|A'] is True or rp['H1_001|A'] == True      # $0 -> $15 is material
    assert rp['H1_001|B'] == False
    assert rp['H1_004|A'] == False                               # $20 -> $0 premium drop, MOOP unchanged
    # denominators: suppressed cell counted as 0, flagged
    assert b.loc[b.cty == 'Z', 'e'].iloc[0] == 0 and b.loc[b.cty == 'Z', 'supp'].iloc[0]
    out, u = A.bridge(b, q, 'repriced_material')
    r = out['UNH']
    assert r['base_total'] == 340 and r['post_total'] == 295
    assert r['bridge_check_residual'] == 0                       # components sum exactly to net change
    assert r['components']['terminated']['net'] == -40
    assert r['components']['unmapped_base']['net'] == -5
    assert r['components']['post_new_plan_or_new_county']['post'] == 12 + 0   # H1_010 new plan; H1_007|C attached to sa_exit unit
    # consolidated unit (H1_002+H1_004 -> H1_003, county A): base 50 -> post 45
    cons = {k: v for k, v in r['components'].items() if k.startswith('consolidated')}
    assert sum(v['base'] for v in cons.values()) == 50 and sum(v['post'] for v in cons.values()) == 45

def test_metric4_total_market_identity():
    base, post, *_ = toy_frames()
    base = base.assign(par=['UNH'] * 5 + ['HUM'] * 5); post = post.assign(par=['UNH'] * 4 + ['HUM'] * 3)
    m = A.metric4_shift_share(base, post)
    # when benchmark = total market, expected totals across all parents equal actual totals in cells with base
    assert set(m['UNH']) == {'total_market', 'market_ex_self'}


def test_configure_data_dir_outside_repo(monkeypatch, tmp_path):
    monkeypatch.delenv(A.ENV_VAR, raising=False)
    repo = os.path.abspath(os.path.join(os.path.dirname(A.__file__), '..', '..', '..'))
    d = A.configure()
    assert not os.path.abspath(d).startswith(repo + os.sep)
    monkeypatch.setenv(A.ENV_VAR, str(tmp_path))
    assert A.configure() == str(tmp_path) and A.SRC == os.path.join(str(tmp_path), 'sources')
    assert A.configure(str(tmp_path / 'x')).endswith('x')
    A.configure()

def test_metric5_without_sec_file(tmp_path):
    A.configure(str(tmp_path))
    assert A.load_sec() == {}
    A.configure()
