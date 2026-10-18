"""Enrollment-weighted Medicare Advantage plan-exposure and membership bridge, CY2025 -> CY2026.

Deterministic. Inputs: official CMS public files placed under <data-dir>/sources/ (see README.md).
Outputs: <data-dir>/outputs/*.json / *.csv. Outputs are research inputs, not verified facts; they need an
independent evidence check before any canonical admission.
Aggregate CMS data shows exposure and NET changes only; it cannot show individual switching or causation.

Data directory: --data-dir CLI argument, else env IIP_MA_ENROLLMENT_DATA, else ~/iip-ma-enrollment-data
(always outside the repository).
"""
import argparse, os, glob, json, re, pickle
import numpy as np, pandas as pd

ENV_VAR = 'IIP_MA_ENROLLMENT_DATA'
DEFAULT_DATA_DIR = os.path.join(os.path.expanduser('~'), 'iip-ma-enrollment-data')
DATA_DIR = SRC = OUT = CACHE = None

def configure(data_dir=None):
    """Set module data paths. Priority: argument > env var > default (outside the repo)."""
    global DATA_DIR, SRC, OUT, CACHE
    DATA_DIR = os.path.abspath(os.path.expanduser(data_dir or os.environ.get(ENV_VAR) or DEFAULT_DATA_DIR))
    SRC = os.path.join(DATA_DIR, 'sources'); OUT = os.path.join(DATA_DIR, 'outputs'); CACHE = os.path.join(OUT, 'cache')
    return DATA_DIR

configure()
PARENTS = {'UnitedHealth Group, Inc.': 'UNH', 'Humana Inc.': 'HUM', 'CVS Health Corporation': 'CVS',
           'Elevance Health, Inc.': 'ELV', 'Centene Corporation': 'CNC'}
PEERS = ['UNH', 'HUM', 'CVS', 'ELV', 'CNC']
MA_ORG_TYPES = {'Local CCP', 'Regional CCP', 'PFFS', 'MSA'}   # MA proper; excludes Cost, PACE, PDP, MMP demos
CONT_STATUSES = {'Renewal Plan', 'Renewal Plan with SAR', 'Renewal Plan with SAE', 'Consolidated Renewal Plan'}
TERM_STATUS = 'Terminated/Non-renewed Contract'
# Repricing definitions (applied at plan-county level, successor vs predecessor in the same county)
ANY = dict(prem=0.0, moop=0.0)                 # plan-count benefit study definition: any premium or MOOP increase, or core supplemental removed
MATERIAL = dict(prem=10.0, moop=500.0)         # material: premium +>=$10/mo or $0 -> >$0; MOOP +>=$500; or core supplemental removed

def pkey(c, p): return c.astype(str).str.strip() + '_' + p.astype(str).str.strip().str.zfill(3)

def norm_county(s):
    s = s.fillna('').str.upper().str.replace(r'[\.\'\-]', '', regex=True)
    s = s.str.replace(r'\b(COUNTY|PARISH|BOROUGH|CENSUS AREA|MUNICIPALITY|CITY AND BOROUGH)\b', '', regex=True)
    s = s.str.replace(r'\bSAINT\b', 'ST', regex=True).str.replace(r'\s+', '', regex=True)
    return s

def parent_code(s): return s.map(PARENTS).fillna('OTHER')

# ---------------- loaders ----------------
def _cached(name, fn):
    os.makedirs(CACHE, exist_ok=True); f = os.path.join(CACHE, name + '.pkl')
    if os.path.exists(f): return pickle.load(open(f, 'rb'))
    x = fn(); pickle.dump(x, open(f, 'wb')); return x

def parse_enroll(s):
    """'*' or blank -> NaN (suppressed: 10 or fewer); else int."""
    return pd.to_numeric(s.astype(str).str.replace(',', '').str.strip().replace({'*': None, '': None}), errors='coerce')

def load_cpsc(ym):
    def f():
        d = os.path.join(SRC, 'cpsc', f'CPSC_Enrollment_{ym[:4]}_{ym[5:]}')
        ci = pd.read_csv(glob.glob(d + '/CPSC_Contract_Info_*.csv')[0], dtype=str, encoding='latin1')
        en = pd.read_csv(glob.glob(d + '/CPSC_Enrollment_Info_*.csv')[0], dtype=str, encoding='latin1')
        ci = ci[ci['Organization Type'].isin(MA_ORG_TYPES)].copy()
        ci['plan'] = pkey(ci['Contract ID'], ci['Plan ID'])
        ci = ci.drop_duplicates('plan')
        en['plan'] = pkey(en['Contract Number'], en['Plan ID'])
        en = en.merge(ci[['plan', 'Organization Type', 'Plan Type', 'Offers Part D', 'SNP Plan', 'EGHP', 'Parent Organization']], on='plan', how='inner')
        en['enr'] = parse_enroll(en['Enrollment']); en['supp'] = en['enr'].isna()
        en['par'] = parent_code(en['Parent Organization'])
        en['ssa'] = en['SSA State County Code'].str.strip()
        en['cty'] = en['State'].fillna('').str.strip() + '|' + norm_county(en['County'])
        en['group'] = en['EGHP'].eq('Yes'); en['snp'] = en['SNP Plan'].eq('Yes')
        en['ptype'] = np.where(en['Plan Type'].str.contains('PPO'), 'PPO', np.where(en['Plan Type'].str.contains('HMO'), 'HMO', 'OTHER'))
        cols = ['plan', 'ssa', 'cty', 'State', 'par', 'Parent Organization', 'group', 'snp', 'ptype', 'Plan Type', 'enr', 'supp']
        return en[cols].reset_index(drop=True)
    return _cached('cpsc_' + ym, f)

def load_contract_totals(ym):
    fs = glob.glob(os.path.join(SRC, 'contract', '**', f'Monthly_Report_By_Contract_{ym[:4]}_{ym[5:]}.csv'), recursive=True)
    d = pd.read_csv(fs[0], dtype=str, encoding='latin1')
    d = d[d['Organization Type'].isin(MA_ORG_TYPES)].copy()
    d['enr'] = parse_enroll(d['Enrollment']); d['par'] = parent_code(d['Parent Organization'])
    return d

def load_crosswalk():
    cw = pd.read_csv(os.path.join(SRC, 'reused', 'PlanCrosswalk2026_10012025.txt'), sep='\t', dtype=str, encoding='latin1')
    cw = cw.dropna(subset=['PREVIOUS_CONTRACT_ID']).copy()
    cw['prev'] = pkey(cw.PREVIOUS_CONTRACT_ID, cw.PREVIOUS_PLAN_ID)
    cw['cur'] = np.where(cw.STATUS.isin(CONT_STATUSES), pkey(cw.CURRENT_CONTRACT_ID.fillna(''), cw.CURRENT_PLAN_ID.fillna('')), None)
    return cw[['prev', 'cur', 'STATUS']]

def load_landscape(year):
    def f():
        fn = {2025: 'CY2025_Landscape_202506.1.csv', 2026: 'CY2026_Landscape_202509.csv'}[year]
        st = {2025: 'State Abbreviation', 2026: 'State Territory Abbreviation'}[year]
        cols = ['Contract Category Type', st, 'County Name', 'Contract ID', 'Plan ID', 'Segment ID',
                'Parent Organization Name', 'Plan Type', 'Special Needs Plan (SNP) Indicator',
                'Monthly Consolidated Premium (Part C + D)', 'In-Network Maximum Out-of-Pocket (MOOP) Amount']
        d = pd.read_csv(os.path.join(SRC, 'reused', fn), dtype=str, encoding='latin1', usecols=cols)
        d = d[d['Contract Category Type'].isin(['MA-PD', 'MA', 'SNP'])].copy()
        d['plan'] = pkey(d['Contract ID'], d['Plan ID'])
        d['seg'] = d['plan'] + '_' + d['Segment ID'].astype(int).astype(str)
        d['cty'] = d[st].str.strip() + '|' + norm_county(d['County Name'])
        num = lambda c: pd.to_numeric(d[c].str.replace(r'[$,\s]', '', regex=True), errors='coerce')
        d['prem'] = num('Monthly Consolidated Premium (Part C + D)'); d['moop'] = num('In-Network Maximum Out-of-Pocket (MOOP) Amount')
        return d[['plan', 'seg', 'cty', 'prem', 'moop']].drop_duplicates(['plan', 'cty', 'seg'])
    return _cached(f'land_{year}', f)

def pbp_core_supp(year):
    """Core supplemental flags per segment (prior PBP benefit-study definitions): dental preventive/comprehensive (mandatory), eyewear, OTC (mandatory)."""
    def f():
        p = os.path.join(SRC, 'reused', f'pbp{year}')
        def rd(n):
            x = pd.read_csv(f'{p}/{n}.txt', sep='\t', dtype=str, encoding='latin1')
            x['seg'] = x.pbp_a_hnumber + '_' + x.pbp_a_plan_identifier.str.zfill(3) + '_' + x.segment_id.astype(int).astype(str)
            return x.drop_duplicates('seg').set_index('seg')
        b16, b17, b13 = rd('pbp_b16_dental'), rd('pbp_b17_eye_exams_wear'), rd('pbp_b13_other_services')
        mand = lambda df, cols: df[cols].isin(['2', '4']).any(axis=1)
        pv = [c for c in b16.columns if c.startswith('pbp_b16b_bendesc_') and c.endswith('_amo')]
        cp = [c for c in b16.columns if c.startswith('pbp_b16c_bendesc_') and c.endswith('_amo')]
        idx = b16.index.union(b17.index).union(b13.index)
        r = pd.DataFrame(index=idx)
        r['dental_prev'] = mand(b16, pv).reindex(idx, fill_value=False)
        r['dental_comp'] = mand(b16, cp).reindex(idx, fill_value=False)
        r['eyewear'] = b17.pbp_b17b_bendesc_yn.eq('1').reindex(idx, fill_value=False)
        r['otc'] = (b13.pbp_b13b_bendesc_otc.eq('1') & b13.pbp_b13b_bendesc_amo.isin(['2', '4'])).reindex(idx, fill_value=False)
        return r.astype(bool)
    return _cached(f'pbp_{year}', f)

# ---------------- crosswalk components ----------------
def components(cw):
    """Union-find over crosswalk edges prev->cur (continuing statuses). Returns dict node->component id.
    Nodes are 'P:<plan>' (2025) and 'C:<plan>' (2026)."""
    par = {}
    def find(a):
        par.setdefault(a, a)
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: par[max(ra, rb)] = min(ra, rb)
    for r in cw.itertuples():
        find('P:' + r.prev)
        if isinstance(r.cur, str): union('P:' + r.prev, 'C:' + r.cur)
    return {k: find(k) for k in list(par)}

def classify_plans(cw):
    """2025 plan -> status class: 'terminated' | 'continuing' (renewal/SAR/SAE/consolidated) ; plus status string."""
    g = cw.groupby('prev').agg(statuses=('STATUS', lambda s: '|'.join(sorted(set(s)))), any_cont=('cur', lambda s: s.notna().any()))
    g['cls'] = np.where(g.any_cont, 'continuing', np.where(g.statuses.str.contains('Terminated'), 'terminated', 'other'))
    g['consolidated'] = g.statuses.str.contains('Consolidated')
    g['sar'] = g.statuses.str.contains('SAR')
    return g

# ---------------- core bridge ----------------
def build_bridge(base, post, cw, L5, L6, S5=None, S6=None):
    """Classify every base-month MA cell (plan x county) and attach the post-month outcome.
    Returns (cells_base, cells_post). Suppressed cells counted as 0 members (reported separately)."""
    comp = components(cw); pc = classify_plans(cw)
    b = base[base.par.isin(PEERS)].copy(); b['e'] = b.enr.fillna(0)
    D5 = {} if S5 is None else {k: v for k, v in zip(S5.index, S5.values)}
    D6 = {} if S6 is None else {k: v for k, v in zip(S6.index, S6.values)}
    b = b.join(pc[['cls', 'statuses', 'consolidated', 'sar']], on='plan')
    b['cls'] = b['cls'].fillna('unmapped')
    b['comp'] = b.plan.map(lambda p: comp.get('P:' + p))
    # in-service-area 2025 (individual plans only; EGWP plans are not in Landscape)
    sa5 = set(zip(L5.plan, L5.cty)); sa6 = set(zip(L6.plan, L6.cty))
    b['in_sa25'] = [(p, c) in sa5 for p, c in zip(b.plan, b.cty)]
    # successors offered in county 2026
    succ = cw[cw.cur.notna()].groupby('prev').cur.apply(lambda s: sorted(set(s))).to_dict()
    b['succ_in_cty'] = [any((s, c) in sa6 for s in succ.get(p, [])) for p, c in zip(b.plan, b.cty)]
    # premium/MOOP: 2025 plan-county value vs successor-in-county value (mean over segments)
    lp5 = L5.groupby(['plan', 'cty'])[['prem', 'moop']].mean(); lp6 = L6.groupby(['plan', 'cty'])[['prem', 'moop']].mean()
    seg5 = L5.groupby(['plan', 'cty']).seg.apply(list).to_dict(); seg6 = L6.groupby(['plan', 'cty']).seg.apply(list).to_dict()
    LP6 = {k: (r[0], r[1]) for k, r in zip(lp6.index, lp6[['prem', 'moop']].values)}
    def succ_vals(p, c):
        v = [LP6[(s, c)] for s in succ.get(p, []) if (s, c) in LP6]
        return (np.mean([x[0] for x in v]), np.mean([x[1] for x in v])) if v else (np.nan, np.nan)
    def supp_removed(p, c):
        if S5 is None: return np.nan
        a = [D5[s] for s in seg5.get((p, c), []) if s in D5]
        z = [D6[s] for sp in succ.get(p, []) for s in seg6.get((sp, c), []) if s in D6]
        if not a or not z: return np.nan
        a = np.any(a, axis=0); z = np.any(z, axis=0)
        return bool((a & ~z).any())
    keys = pd.MultiIndex.from_arrays([b.plan, b.cty])
    v5 = lp5.reindex(keys)
    b['prem25'] = v5.prem.values; b['moop25'] = v5.moop.values
    need = b.cls.eq('continuing') & b.in_sa25 & b.succ_in_cty & ~b.group
    sv = {(p, c): succ_vals(p, c) for p, c in set(zip(b.plan[need], b.cty[need]))}
    sr = {(p, c): supp_removed(p, c) for p, c in set(zip(b.plan[need], b.cty[need]))}
    b['prem26'] = [sv.get((p, c), (np.nan, np.nan))[0] for p, c in zip(b.plan, b.cty)]
    b['moop26'] = [sv.get((p, c), (np.nan, np.nan))[1] for p, c in zip(b.plan, b.cty)]
    b['supp_removed'] = [sr.get((p, c), np.nan) for p, c in zip(b.plan, b.cty)]
    b['seg_class'] = segment_class(b)
    b['repriced_any'] = reprice_flag(b, ANY); b['repriced_material'] = reprice_flag(b, MATERIAL)
    # outcome cells
    q = post[post.par.isin(PEERS)].copy(); q['e'] = q.enr.fillna(0)
    q['comp'] = q.plan.map(lambda p: comp.get('C:' + p))
    return b, q

def segment_class(b):
    """Exposure class per base cell."""
    c = np.select(
        [b.cls.eq('unmapped').values, b.cls.eq('terminated').values, b.cls.eq('other').values,
         b.group.values, ~b.in_sa25.values, ~b.succ_in_cty.values, b.consolidated.fillna(False).astype(bool).values],
        ['unmapped', 'terminated', 'other_status', 'group_continuing', 'out_of_area_residence', 'sa_exit', 'consolidated'],
        default='renewal')
    return pd.Series(c, index=b.index)

def reprice_flag(b, th):
    """True/False/NaN for individual continuing in-area cells (renewal or consolidated)."""
    dp = b.prem26 - b.prem25; dm = b.moop26 - b.moop25
    prem_up = (dp > th['prem']) if th['prem'] == 0 else ((dp >= th['prem']) | ((b.prem25 == 0) & (b.prem26 > 0)))
    moop_up = (dm > th['moop']) if th['moop'] == 0 else (dm >= th['moop'])
    flag = prem_up | moop_up | b.supp_removed.fillna(False).astype(bool)
    known = b.prem25.notna() & b.prem26.notna()
    out = pd.Series(np.where(known, flag, np.nan), index=b.index, dtype=object)
    out[~b.seg_class.isin(['renewal', 'consolidated'])] = np.nan
    return out

def component_county_outcome(b, q, keys=('comp', 'cty')):
    """Net change in continuing component-county units: base (predecessors) vs post (successors), same county."""
    k = list(keys)
    bb = b[b.comp.notna()].groupby(k).e.sum().rename('base')
    qq = q[q.comp.notna()].groupby(k).e.sum().rename('post')
    return pd.concat([bb, qq], axis=1).fillna(0)

# ---------------- metric builders ----------------
def metric1_exposure(b):
    rows = []
    for p in PEERS:
        x = b[b.par == p]; tot = x.e.sum()
        for (sc, gr, sn, pt), h in x.groupby(['seg_class', 'group', 'snp', 'ptype']):
            rows.append(dict(parent=p, seg_class=sc, group=bool(gr), snp=bool(sn), ptype=pt, members=int(h.e.sum()), cells=len(h), suppressed_cells=int(h.supp.sum()), parent_total=int(tot)))
    return pd.DataFrame(rows)

def exposure_summary(b):
    out = {}
    for p in PEERS:
        x = b[b.par == p]; tot = x.e.sum(); ind = x[~x.group]
        s = x.groupby('seg_class').e.sum()
        cont = ind[ind.seg_class.isin(['renewal', 'consolidated'])]
        sg = x.groupby(['seg_class', 'group']).e.sum()
        out[p] = dict(total=int(tot), individual=int(ind.e.sum()),
                      by_class={k: int(v) for k, v in s.items()},
                      by_class_individual={k: int(v) for (k, g), v in sg.items() if not g},
                      by_class_group={k: int(v) for (k, g), v in sg.items() if g},
                      by_class_ptype={f'{k}|{pt}': int(v) for (k, pt), v in x.groupby(['seg_class', 'ptype']).e.sum().items()},
                      share_terminated=round(s.get('terminated', 0) / tot, 4),
                      share_sa_exit=round(s.get('sa_exit', 0) / tot, 4),
                      share_term_or_sa_exit=round((s.get('terminated', 0) + s.get('sa_exit', 0)) / tot, 4),
                      share_consolidated=round(s.get('consolidated', 0) / tot, 4),
                      repriced_any_members=int(cont[cont.repriced_any == True].e.sum()),
                      repriced_material_members=int(cont[cont.repriced_material == True].e.sum()),
                      notrepriced_any_members=int(cont[cont.repriced_any == False].e.sum()),
                      notrepriced_material_members=int(cont[cont.repriced_material == False].e.sum()),
                      pricing_unknown_members=int(cont[cont.repriced_any.isna()].e.sum()),
)
    return out

def metric2_continuing(b, q, flag='repriced_any'):
    """Plan-county units (component x county) for individual continuing in-area cells, split by repricing flag.
    Unit flag = enrollment-weighted majority of predecessor cells (flag True if >=50% of base members flagged)."""
    rows = {}
    ind = b[b.seg_class.isin(['renewal', 'consolidated'])].copy()
    ind['f'] = ind[flag].map({True: 1.0, False: 0.0})
    u = ind.groupby(['par', 'comp', 'cty']).apply(lambda g: pd.Series(dict(base=g.e.sum(), fshare=np.average(g.f.dropna(), weights=g.e[g.f.notna()]) if g.f.notna().any() and g.e[g.f.notna()].sum() > 0 else np.nan)), include_groups=False).reset_index()
    post = q[q.comp.notna()].groupby(['comp', 'cty']).e.sum().rename('post')
    u = u.join(post, on=['comp', 'cty']); u['post'] = u.post.fillna(0)
    u['grp'] = np.where(u.fshare.isna(), 'unknown', np.where(u.fshare >= 0.5, 'repriced', 'not_repriced'))
    for p in PEERS:
        x = u[u.par == p]; r = {}
        for gname, g in x.groupby('grp'):
            r[gname] = dict(units=len(g), base=int(g.base.sum()), post=int(g.post.sum()), net=int(g.post.sum() - g.base.sum()),
                            pct=round((g.post.sum() - g.base.sum()) / g.base.sum(), 4) if g.base.sum() else None)
        tb, tp = x.base.sum(), x.post.sum()
        r['all_continuing'] = dict(units=len(x), base=int(tb), post=int(tp), net=int(tp - tb), pct=round((tp - tb) / tb, 4) if tb else None)
        rows[p] = r
    return rows, u

def parent_totals(df):
    return df.groupby('par').agg(members=('e' if 'e' in df else 'enr', 'sum'), supp_cells=('supp', 'sum'), cells=('supp', 'size'))

def metric3_county_share(b, q, base_df, post_df):
    """UNH share in counties where UNH has >=1 individual continuing in-area plan-county (base), base vs post; peer net change there."""
    cont_cty = set(b[(b.par == 'UNH') & b.seg_class.isin(['renewal', 'consolidated'])].ssa)
    def agg(df):
        d = df[df.ssa.isin(cont_cty)]
        return d.groupby('par').enr.sum()
    a, z = agg(base_df), agg(post_df)
    tot_a, tot_z = a.sum(), z.sum()
    res = dict(n_counties=len(cont_cty), market_base=int(tot_a), market_post=int(tot_z), market_net=int(tot_z - tot_a),
               market_pct=round((tot_z - tot_a) / tot_a, 4))
    for p in PEERS + ['OTHER']:
        res[p] = dict(base=int(a.get(p, 0)), post=int(z.get(p, 0)), net=int(z.get(p, 0) - a.get(p, 0)),
                      pct=round((z.get(p, 0) - a.get(p, 0)) / a.get(p, 1), 4), share_base=round(a.get(p, 0) / tot_a, 4), share_post=round(z.get(p, 0) / tot_z, 4))
    return res, cont_cty

def county_level_test(b, base_df, post_df):
    """Counties classified by UNH individual exit exposure (terminated + sa_exit share of UNH base members in county).
    For each bucket: UNH, peer and market-ex-UNH net % change. Tests whether UNH loses even where it withdrew nothing."""
    ub = b[(b.par == 'UNH') & ~b.group]
    ex = ub[ub.seg_class.isin(['terminated', 'sa_exit'])].groupby('ssa').e.sum()
    tot = ub.groupby('ssa').e.sum()
    share = (ex.reindex(tot.index).fillna(0) / tot.replace(0, np.nan)).fillna(0)
    bucket = pd.cut(share, [-0.001, 0.0, 0.10, 0.30, 1.0], labels=['0%', '0-10%', '10-30%', '>30%'])
    ind_a = base_df[~base_df.group]; ind_z = post_df[~post_df.group]
    A = ind_a.groupby(['ssa', 'par']).enr.sum().unstack(fill_value=0); Z = ind_z.groupby(['ssa', 'par']).enr.sum().unstack(fill_value=0)
    out = {}
    for bk in bucket.cat.categories:
        cs = bucket[bucket == bk].index
        a = A.reindex(cs).fillna(0).sum(); z = Z.reindex(cs).fillna(0).sum()
        r = dict(n_counties=int(len(cs)))
        for p in PEERS + ['OTHER']:
            r[p] = dict(base=int(a.get(p, 0)), post=int(z.get(p, 0)), net=int(z.get(p, 0) - a.get(p, 0)), pct=round((z.get(p, 0) - a.get(p, 0)) / a.get(p, 0), 4) if a.get(p, 0) else None)
        r['UNH_exit_exposure_members'] = int(ex.reindex(cs).fillna(0).sum())
        r['market_total_pct'] = round(z.sum() / a.sum() - 1, 4) if a.sum() else None
        mx_a = a.sum() - a.get('UNH', 0); mx_z = z.sum() - z.get('UNH', 0)
        r['market_ex_UNH_pct'] = round((mx_z - mx_a) / mx_a, 4) if mx_a else None
        r['UNH_share_base'] = round(a.get('UNH', 0) / a.sum(), 4) if a.sum() else None
        r['UNH_share_post'] = round(z.get('UNH', 0) / z.sum(), 4) if z.sum() else None
        out[str(bk)] = r
    # within zero-exit counties: split by UNH repriced share (individual continuing, 'any' definition)
    ub2 = ub[ub.seg_class.isin(['renewal', 'consolidated']) & ub.repriced_any.notna()]
    rs = (ub2[ub2.repriced_any == True].groupby('ssa').e.sum().reindex(ub2.ssa.unique()).fillna(0) / ub2.groupby('ssa').e.sum()).fillna(0)
    z0 = bucket[bucket == '0%'].index
    rb = pd.cut(rs.reindex(z0).fillna(0), [-0.001, 0.25, 0.75, 1.0], labels=['repriced<=25%', '25-75%', '>75%'])
    for bk in rb.cat.categories:
        cs = rb[rb == bk].index
        a = A.reindex(cs).fillna(0).sum(); z = Z.reindex(cs).fillna(0).sum()
        r = dict(n_counties=int(len(cs)))
        for p in PEERS + ['OTHER']:
            r[p] = dict(base=int(a.get(p, 0)), post=int(z.get(p, 0)), net=int(z.get(p, 0) - a.get(p, 0)), pct=round((z.get(p, 0) - a.get(p, 0)) / a.get(p, 0), 4) if a.get(p, 0) else None)
        mx_a = a.sum() - a.get('UNH', 0); mx_z = z.sum() - z.get('UNH', 0)
        r['market_total_pct'] = round(z.sum() / a.sum() - 1, 4) if a.sum() else None
        r['market_ex_UNH_pct'] = round((mx_z - mx_a) / mx_a, 4) if mx_a else None
        r['UNH_share_base'] = round(a.get('UNH', 0) / a.sum(), 4) if a.sum() else None
        r['UNH_share_post'] = round(z.get('UNH', 0) / z.sum(), 4) if z.sum() else None
        out['zero_exit|' + str(bk)] = r
    return out

def metric4_shift_share(base_df, post_df):
    """Actual vs expected post enrollment per parent, matched on county x group x SNP x plan type.
    Expected = parent base in cell x (benchmark growth in same cell). Benchmarks: 'total_market' (all MA orgs incl. the parent;
    primary - answers 'did the cell market itself shrink?') and 'market_ex_self' (competitors only; mechanically inflated when the
    parent loses members because the same members show up as competitor gains). Cells with benchmark base <50 fall back to
    national segment (group x SNP x ptype) benchmark growth."""
    seg = ['group', 'snp', 'ptype']
    A = base_df.groupby(['ssa'] + seg + ['par']).enr.sum(); Z = post_df.groupby(['ssa'] + seg + ['par']).enr.sum()
    M = pd.concat([A.rename('a'), Z.rename('z')], axis=1).fillna(0).reset_index()
    res = {}
    for p in PEERS:
      for bench in ['total_market', 'market_ex_self']:
        own = M[M.par == p].set_index(['ssa'] + seg)[['a', 'z']]
        mk = M if bench == 'total_market' else M[M.par != p]
        oth = mk.groupby(['ssa'] + seg)[['a', 'z']].sum()
        nat = mk.groupby(seg)[['a', 'z']].sum(); nat_g = (nat.z / nat.a)
        j = own.join(oth, rsuffix='_mkt', how='left').fillna(0)
        g = np.where(j.a_mkt >= 50, j.z_mkt / j.a_mkt.replace(0, np.nan), np.nan)
        fb = nat_g.reindex(pd.MultiIndex.from_arrays([j.index.get_level_values(k) for k in seg])).values
        j['g'] = np.where(np.isnan(g), fb, g); j['exp'] = j.a * j.g
        r = dict(base=int(j.a.sum()), actual_post=int(j.z.sum()), expected_post=int(round(j.exp.sum())),
                 actual_pct=round(j.z.sum() / j.a.sum() - 1, 4), expected_pct=round(j.exp.sum() / j.a.sum() - 1, 4),
                 gap_members=int(round(j.z.sum() - j.exp.sum())), share_base_cells_fallback=round(j.a[np.isnan(g)].sum() / j.a.sum(), 4))
        r['note_new_cells'] = 'actual_post includes cells where parent had 0 base (entries); expected assigns 0 there'
        for dim in seg:
            r['by_' + dim] = {}
            for k, h in j.groupby(level=dim):
                r['by_' + dim][str(k)] = dict(base=int(h.a.sum()), actual_post=int(h.z.sum()), expected_post=int(round(h.exp.sum())),
                                              actual_pct=round(h.z.sum() / h.a.sum() - 1, 4) if h.a.sum() else None,
                                              expected_pct=round(h.exp.sum() / h.a.sum() - 1, 4) if h.a.sum() else None)
        res.setdefault(p, {})[bench] = r
    return res

CLASS_PRIORITY = ['terminated', 'sa_exit', 'consolidated', 'renewal', 'group_continuing', 'out_of_area_residence', 'other_status']

def bridge(b, q, flag='repriced_any'):
    """Net change per parent = sum over (component x county) units of (post - base) + unmapped base (-) + unmatched post (+).
    Unit class = class of its largest base cell; individual continuing units split by repricing flag (>=50% of base members)."""
    x = b[b.comp.notna()].copy()
    x['f'] = x[flag].map({True: 1.0, False: 0.0})
    x['fw'] = x.f * x.e; x['fe'] = np.where(x.f.notna(), x.e, 0)
    x['rank'] = x.groupby(['comp', 'cty']).e.rank(method='first', ascending=False)
    top = x[x['rank'] == 1].set_index(['comp', 'cty'])[['seg_class', 'par', 'ptype', 'snp', 'group']]
    u = x.groupby(['comp', 'cty']).agg(base=('e', 'sum'), fw=('fw', 'sum'), fe=('fe', 'sum')).join(top)
    pq = q[q.comp.notna()].groupby(['comp', 'cty']).e.sum().rename('post')
    u = u.join(pq, how='left'); u['post'] = u.post.fillna(0)
    u['cls'] = u.seg_class
    ind = u.cls.isin(['renewal', 'consolidated'])
    rs = u.fw / u.fe.replace(0, np.nan)
    u.loc[ind, 'cls'] = np.where(rs[ind].isna(), u.cls[ind] + '|pricing_unknown', np.where(rs[ind] >= 0.5, u.cls[ind] + '|repriced', u.cls[ind] + '|not_repriced'))
    # post cells not attached to any base unit
    qk = q.set_index(['comp', 'cty']).index
    in_unit = qk.isin(u.index) & q.comp.notna().values
    q_un = q[~in_unit]
    out = {}
    for p in PEERS:
        uu = u[u.par == p]
        rows = {}
        for c, g in uu.groupby('cls'):
            rows[c] = dict(units=int(len(g)), base=int(g.base.sum()), post=int(g.post.sum()), net=int(g.post.sum() - g.base.sum()))
        ub = b[(b.par == p) & b.comp.isna()].e.sum()
        rows['unmapped_base'] = dict(base=int(ub), post=0, net=-int(ub))
        qp = q_un[q_un.par == p]
        rows['post_new_plan_or_new_county'] = dict(base=0, post=int(qp.e.sum()), net=int(qp.e.sum()),
                                                   of_which_successor_new_county=int(qp[qp.comp.notna()].e.sum()),
                                                   of_which_plan_not_in_crosswalk_as_successor=int(qp[qp.comp.isna()].e.sum()))
        tb = b[b.par == p].e.sum(); tp = q[q.par == p].e.sum()
        chk = sum(r['net'] for r in rows.values())
        byseg = {}
        for (c, pt, sn), g in uu.groupby(['cls', 'ptype', 'snp']):
            byseg[f'{c}|{pt}|{"SNP" if sn else "nonSNP"}'] = dict(base=int(g.base.sum()), post=int(g.post.sum()), net=int(g.post.sum() - g.base.sum()))
        out[p] = dict(base_total=int(tb), post_total=int(tp), net=int(tp - tb), components=rows, bridge_check_residual=int(tp - tb - chk),
                      components_by_ptype_snp=byseg)
        # parent-attribution note: units are assigned to the parent of the largest base cell; post of a successor owned by another parent
        # (rare contract transfers) is attributed to that unit.
    return out, u

def load_sec():
    """SEC-reported MA membership (thousands) per parent, read from <data-dir>/sources/sec_membership.json.
    Format: {"UNH": {"_def": "<definition + filing>", "2025-12-31": <value>, ...}, ...}. Values are typed in by the
    analyst from public 10-K/10-Q/8-K filings and must be quote-checked; none are embedded in this code."""
    f = os.path.join(SRC, 'sec_membership.json')
    return json.load(open(f)) if os.path.exists(f) else {}

# CMS report month whose enrollment best approximates a quarter-end date: CMS monthly report reflects enrollment effective the 1st of
# the month, so SEC period end D ~ CMS report month D+1 (e.g. 2026-03-31 ~ 2026-04). Both shown.
SEC_TO_CMS = {'2024-12-31': ['2024-12', '2025-01'], '2025-03-31': ['2025-03', '2025-04'], '2025-06-30': ['2025-06', '2025-07'],
              '2025-12-31': ['2025-12', '2026-01'], '2026-03-31': ['2026-03', '2026-04'], '2026-06-30': ['2026-06', '2026-07'], '2026-09-30': ['2026-09', '2026-10']}

def metric5_reconcile(months_contract, sec=None):
    SEC = load_sec() if sec is None else sec
    tot = {}
    for ym in months_contract:
        d = load_contract_totals(ym)
        g = d.groupby('par').enr.sum()
        tot[ym] = {p: int(g.get(p, 0)) for p in PEERS}
        sp = d[d.enr.isna()].groupby('par').size(); tot[ym]['_suppressed_contracts'] = {p: int(sp.get(p, 0)) for p in PEERS}
        # group (EGWP) not identifiable in contract file; see CPSC-based split
    rec = {}
    for p in PEERS:
        if p not in SEC: continue
        r = {}
        for dt, v in SEC[p].items():
            if dt.startswith('_'): continue
            cms = {m: tot[m][p] for m in SEC_TO_CMS.get(dt, []) if m in tot}
            r[dt] = dict(sec_k=v, cms_contract_total=cms, cms_minus_sec_pct={m: round(c / 1000 / v - 1, 4) for m, c in cms.items()})
        dts = [k for k in SEC[p] if not k.startswith('_')]
        rec[p] = dict(definition=SEC[p].get('_def'), points=r)
    return tot, rec

def cpsc_suppression(df, ym, ct):
    """Suppressed share per parent: contract-file total vs sum of unsuppressed CPSC cells."""
    s = df.groupby('par').enr.sum(); c = ct.groupby('par').enr.sum(); n = df[df.supp].groupby('par').size()
    return {p: dict(cpsc_unsuppressed_sum=int(s.get(p, 0)), contract_file_total=int(c.get(p, 0)),
                    suppressed_members_est=int(c.get(p, 0) - s.get(p, 0)), suppressed_share=round(1 - s.get(p, 0) / c.get(p, 1), 4),
                    suppressed_cells=int(n.get(p, 0))) for p in PEERS}

def segment_totals(df):
    r = {}
    for p in PEERS:
        x = df[df.par == p]; t = x.enr.sum()
        r[p] = dict(total=int(t), group=int(x[x.group].enr.sum()), individual=int(x[~x.group].enr.sum()),
                    snp=int(x[x.snp].enr.sum()), nonsnp=int(x[~x.snp].enr.sum()),
                    individual_nonsnp=int(x[~x.group & ~x.snp].enr.sum()), individual_snp=int(x[~x.group & x.snp].enr.sum()),
                    hmo=int(x[x.ptype == 'HMO'].enr.sum()), ppo=int(x[x.ptype == 'PPO'].enr.sum()), other=int(x[x.ptype == 'OTHER'].enr.sum()))
    mk = df.enr.sum(); r['MARKET_MA'] = dict(total=int(mk), group=int(df[df.group].enr.sum()), snp=int(df[df.snp].enr.sum()))
    return r

def count_vs_enrollment(b):
    """Count-weighted (share of 2025 individual in-area plan-county cells) vs enrollment-weighted share exposed to termination/SA exit."""
    r = {}
    x = b[~b.group & b.in_sa25]
    for p in PEERS:
        y = x[x.par == p]; ex = y.seg_class.isin(['terminated', 'sa_exit'])
        plans = y.groupby('plan').agg(term=('seg_class', lambda s: (s == 'terminated').all()), e=('e', 'sum'))
        r[p] = dict(cells=len(y), count_share_cells_exposed=round(ex.mean(), 4), enroll_share_exposed=round(y.e[ex].sum() / y.e.sum(), 4),
                    plans=len(plans), count_share_plans_terminated=round(plans.term.mean(), 4),
                    enroll_share_in_terminated_plans=round(plans.e[plans.term].sum() / plans.e.sum(), 4),
                    count_share_cells_repriced_any=round((y.repriced_any == True).sum() / y.repriced_any.notna().sum(), 4),
                    enroll_share_repriced_any=round(y.e[y.repriced_any == True].sum() / y.e[y.repriced_any.notna()].sum(), 4),
                    count_share_cells_repriced_material=round((y.repriced_material == True).sum() / y.repriced_material.notna().sum(), 4),
                    enroll_share_repriced_material=round(y.e[y.repriced_material == True].sum() / y.e[y.repriced_material.notna()].sum(), 4))
        k = y[y.seg_class.isin(['renewal', 'consolidated']) & y.prem25.notna() & y.prem26.notna()]
        up = k.prem26 > k.prem25; up10 = (k.prem26 - k.prem25 >= 10) | ((k.prem25 == 0) & (k.prem26 > 0))
        r[p].update(premium_only=dict(cells=len(k), count_share_cells_premium_up=round(up.mean(), 4), enroll_share_premium_up=round(k.e[up].sum() / k.e.sum(), 4),
                                      count_share_cells_premium_up_material=round(up10.mean(), 4), enroll_share_premium_up_material=round(k.e[up10].sum() / k.e.sum(), 4),
                                      enroll_weighted_mean_premium_change=round(float(np.average(k.prem26 - k.prem25, weights=k.e)) if k.e.sum() else np.nan, 2),
                                      enroll_share_zero_premium_25=round(k.e[k.prem25 == 0].sum() / k.e.sum(), 4), enroll_share_zero_premium_26=round(k.e[k.prem26 == 0].sum() / k.e.sum(), 4)))
    return r

def jd(o, f):
    json.dump(o, open(os.path.join(OUT, f), 'w'), indent=1, default=lambda v: None if (isinstance(v, float) and np.isnan(v)) else (int(v) if isinstance(v, (np.integer,)) else float(v)))

def run():
    os.makedirs(OUT, exist_ok=True)
    cw = load_crosswalk(); L5 = load_landscape(2025); L6 = load_landscape(2026)
    S5 = pbp_core_supp(2025); S6 = pbp_core_supp(2026)
    months = ['2025-02', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-09', '2026-10']
    C = {m: load_cpsc(m) for m in months}
    res = {'_meta': dict(primary_comparison='2025-02 -> 2026-02 (default, post-AEP+OEP-start both years)',
                         sensitivities=['2025-12 -> 2026-02 (isolates CY2026 AEP; crosswalk applies to Dec-2025 plans)', '2025-02 -> 2026-10 (latest)'],
                         definitions=dict(MA_org_types=sorted(MA_ORG_TYPES), repriced_any=ANY, repriced_material=MATERIAL,
                                          suppression='CPSC cells with 10 or fewer members are blank (*) -> counted as 0; quantified vs contract-file totals'),
                         caveat='Aggregate net data: shows exposure and net change, not individual switching or causation. UNVERIFIED.')}
    # suppression & segment totals
    supp = {}; seg = {}
    for m in months:
        ct = load_contract_totals(m); supp[m] = cpsc_suppression(C[m], m, ct); seg[m] = segment_totals(C[m])
    jd(supp, 'suppression_by_month.json'); jd(seg, 'segment_totals_by_month.json')
    # landscape join quality
    pairs = {}
    for m in ['2025-02', '2025-12']:
        x = C[m][C[m].par.isin(PEERS) & ~C[m].group]
        lk = set(zip(L5.plan, L5.cty)); hit = [(p, c) in lk for p, c in zip(x.plan, x.cty)]
        pl = set(L5.plan); inl = x.plan.isin(pl)
        pairs[m] = dict(individual_members=int(x.enr.sum()), members_in_plans_in_landscape=int(x.enr[inl].sum()),
                        members_cells_matched_to_landscape_county=int(x.enr[np.array(hit)].sum()))
    res['landscape_join'] = pairs
    for tag, (bm, pm) in {'primary_feb25_feb26': ('2025-02', '2026-02'), 'aep_dec25_feb26': ('2025-12', '2026-02'),
                          'latest_feb25_oct26': ('2025-02', '2026-10'), 'aep_dec25_oct26': ('2025-12', '2026-10')}.items():
        b, q = build_bridge(C[bm], C[pm], cw, L5, L6, S5, S6)
        r = {}
        r['metric1_exposure_summary'] = exposure_summary(b)
        m1 = metric1_exposure(b); m1.to_csv(os.path.join(OUT, f'metric1_exposure_by_class_ptype_{tag}.csv'), index=False)
        r['count_vs_enrollment_weighted'] = count_vs_enrollment(b)
        r['metric2_continuing_any'], u_any = metric2_continuing(b, q, 'repriced_any')
        r['metric2_continuing_material'], _ = metric2_continuing(b, q, 'repriced_material')
        r['metric3_unh_continuing_counties'], _ = metric3_county_share(b, q, C[bm], C[pm])
        r['county_exit_exposure_buckets_individual'] = county_level_test(b, C[bm], C[pm])
        r['metric4_shift_share'] = metric4_shift_share(C[bm], C[pm])
        r['bridge_any'], units = bridge(b, q, 'repriced_any')
        r['bridge_material'], _ = bridge(b, q, 'repriced_material')
        units.reset_index().to_csv(os.path.join(OUT, f'units_{tag}.csv.gz'), index=False, compression='gzip')
        res[tag] = r
    tot, rec = metric5_reconcile(['2024-12', '2025-01', '2025-02', '2025-03', '2025-04', '2025-06', '2025-07', '2025-09', '2025-10', '2025-11',
                                  '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-06', '2026-07', '2026-09', '2026-10'])
    res['metric5_cms_contract_totals_by_month'] = tot; res['metric5_sec_reconciliation'] = rec
    jd(res, 'results.json')
    return res

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--data-dir', help=f'data directory (default: ${ENV_VAR} or {DEFAULT_DATA_DIR})')
    a = ap.parse_args(argv); configure(a.data_dir); run(); print('done; outputs in', OUT)

if __name__ == '__main__':
    main()
