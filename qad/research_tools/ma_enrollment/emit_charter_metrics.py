"""Emit the five evidence-gap metrics (exposure; repriced vs not-repriced continuing units; county share; matched
county x segment comparison; CMS vs SEC reconciliation) from <data-dir>/outputs/results.json into
outputs/charter_metrics.json and outputs/charter_metric1_summary.csv. Deterministic; no new data. Run after analysis.py."""
import argparse, json, os
import pandas as pd
from qad.research_tools.ma_enrollment import analysis as A

def main(argv=None):
    ap = argparse.ArgumentParser(description='Emit evidence-gap metrics from results.json')
    ap.add_argument('--data-dir', help=f'data directory (default: ${A.ENV_VAR} or {A.DEFAULT_DATA_DIR})')
    a = ap.parse_args(argv); A.configure(a.data_dir)
    r = json.load(open(os.path.join(A.OUT, 'results.json')))
    _emit(r, A.OUT, A.PEERS)
    print('ok')

def _emit(r, O, P):
    out = {'_meta': r['_meta'] | {'note': 'Windows: primary Feb-2025->Feb-2026 (default); AEP Dec-2025->Feb-2026 (crosswalk base month); Oct-2026 latest. Members = unsuppressed CPSC cells (suppressed cells counted 0; see metric5.suppression). UNVERIFIED.'}}
    for tag in ['primary_feb25_feb26', 'aep_dec25_feb26', 'aep_dec25_oct26', 'latest_feb25_oct26']:
        x = r[tag]; m = {}
        m1 = {}
        for p in P:
            e = x['metric1_exposure_summary'][p]; ind = e['by_class_individual']
            exp = ind.get('terminated', 0) + ind.get('sa_exit', 0) + e['by_class_group'].get('terminated', 0)
            byp = {}
            for k, v in e['by_class_ptype'].items():
                c, pt = k.split('|')
                if c in ('terminated', 'sa_exit'): byp[pt] = byp.get(pt, 0) + v
            m1[p] = dict(base_members=e['total'], exposed_terminated_or_sa_exit=exp, exposed_pct=round(exp / e['total'], 4),
                         terminated=ind.get('terminated', 0) + e['by_class_group'].get('terminated', 0), sa_exit=ind.get('sa_exit', 0),
                         exposed_by_plan_type=byp, consolidated_into_other_plan=ind.get('consolidated', 0),
                         net_change_total=x['bridge_any'][p]['net'], exposed_as_share_of_net_decline=round(exp / -x['bridge_any'][p]['net'], 4) if x['bridge_any'][p]['net'] < 0 else None,
                         count_vs_enrollment=x['count_vs_enrollment_weighted'][p])
        m['metric1_exposure'] = m1
        m['metric2_continuing_repriced_vs_not'] = {'definition_any': x['metric2_continuing_any'], 'definition_material': x['metric2_continuing_material']}
        m['metric3_unh_continuing_counties'] = x['metric3_unh_continuing_counties']
        m['metric3b_counties_by_unh_exit_exposure'] = x['county_exit_exposure_buckets_individual']
        m['metric4_matched_county_segment'] = {p: {'total_market_benchmark': x['metric4_shift_share'][p]['total_market'],
                                                    'market_ex_self_benchmark': x['metric4_shift_share'][p]['market_ex_self']} for p in P}
        m['bridge_UNH'] = x['bridge_any']['UNH']
        out[tag] = m
    supp = json.load(open(os.path.join(O, 'suppression_by_month.json')))
    out['metric5_cms_vs_sec'] = dict(reconciliation=r['metric5_sec_reconciliation'], cms_contract_totals=r['metric5_cms_contract_totals_by_month'],
                                     suppression=supp, unmapped_base_members={t: {p: r[t]['bridge_any'][p]['components']['unmapped_base']['base'] for p in P} for t in ['primary_feb25_feb26', 'aep_dec25_feb26']},
                                     landscape_county_join=r['landscape_join'])
    json.dump(out, open(os.path.join(O, 'charter_metrics.json'), 'w'), indent=1)
    rows = [dict(window=t, parent=p, **{k: v for k, v in out[t]['metric1_exposure'][p].items() if not isinstance(v, dict)}) for t in ['primary_feb25_feb26', 'aep_dec25_feb26'] for p in P]
    pd.DataFrame(rows).to_csv(os.path.join(O, 'charter_metric1_summary.csv'), index=False)

if __name__ == '__main__':
    main()
