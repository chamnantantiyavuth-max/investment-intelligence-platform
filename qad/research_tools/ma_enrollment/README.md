# MA enrollment exposure tool (CY2025 → CY2026)

Reproducible, deterministic calculation of **enrollment-weighted** Medicare Advantage plan exposure and a membership bridge per parent organisation (UnitedHealth Group, Humana, CVS Health, Elevance Health, Centene):

- members in terminated plans, county service-area exits, consolidations and renewals (crosswalk × Landscape counties);
- continuing plan-county units, split into repriced vs not repriced (premium / MOOP increase, core supplemental removal);
- share change in continuing counties, counties bucketed by exit exposure;
- shift-share matched on county × group/individual × SNP × HMO/PPO;
- CMS reconstruction vs SEC-reported MA membership, with suppressed and unmapped enrollment quantified.

Aggregate CMS data shows **exposure and net change only**. It cannot show that an individual member switched to a given competitor, nor causation. Outputs are research inputs that require an independent evidence check; they are not verified facts.

**This directory contains code only.** Data, source snapshots, outputs and findings are kept in a private data directory outside the repository and must never be committed.

## Data directory
Resolved in this order: `--data-dir` CLI argument → env `IIP_MA_ENROLLMENT_DATA` → `~/iip-ma-enrollment-data`.

```
<data-dir>/
  sources/
    cpsc/      monthly-enrollment-cpsc-<month>-<year>.zip, unzipped (CPSC_Enrollment_YYYY_MM/…)
    contract/  monthly enrollment by contract zips, unzipped (Monthly_Report_By_Contract_YYYY_MM.csv)
    plan/      monthly enrollment by plan zips (optional; cross-check)
    reused/    PlanCrosswalk2026_10012025.txt, CY2025_Landscape_202506.1.csv, CY2026_Landscape_202509.csv,
               pbp2025/ and pbp2026/ (unzipped PBP benefits text files)
    sec_membership.json   analyst-entered SEC MA membership (thousands), e.g.
                          {"UNH": {"_def": "<line item + filing URL>", "2025-12-31": <value>}, ...}
  outputs/     written by the scripts (results.json, csv, cache/)
```

## Official sources (CMS, public)
- **Monthly Enrollment by Contract/Plan/State/County (CPSC):**
  - index: https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/monthly-enrollment-contract/plan/state/county
  - file pattern: `https://www.cms.gov/files/zip/monthly-enrollment-cpsc-<month>-<year>.zip` (e.g. `…-december-2025.zip`)
- **Monthly Enrollment by Contract:**
  - index: https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/monthly-enrollment-contract
  - each month's landing page links its zip; names vary, e.g. `monthly-enrollment-contract-december-2025.zip` and `monthly-report-contract-march-2025.zip`.
- **Monthly Enrollment by Plan:** https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/monthly-enrollment-plan
- **CY2026 Plan Crosswalk:** https://www.cms.gov/files/zip/plan-crosswalk-2026.zip
- **MA Landscape:**
  - CY2026: https://www.cms.gov/files/zip/cy2026-landscape-202509.zip
  - CY2025 (inside the historical archive): https://www.cms.gov/files/zip/cy2006-cy2025-landscape-files.zip
- **PBP benefits:**
  - https://www.cms.gov/files/zip/pbp-benefits-2025.zip
  - https://www.cms.gov/files/zip/pbp-benefits-2026.zip
- **SEC EDGAR 10-K / 10-Q / 8-K** filings of each parent, for `sec_membership.json`. Fetch with a descriptive User-Agent.

Default months used by `analysis.run()`: CPSC 2025-02, 2025-11, 2025-12, 2026-01, 2026-02, 2026-03, 2026-04, 2026-09, 2026-10. Contract files: 2024-12 through 2026-10, as listed in `run()`.

## Regenerate
```bash
export IIP_MA_ENROLLMENT_DATA=/path/outside/repo/ma_enrollment_data
# 1. download the zips above into sources/{cpsc,contract,plan}/ (save each CMS landing page as p_<YYYY-MM>.html
#    next to it so the manifest can record URLs), unzip in place, populate sources/reused/ and sec_membership.json
# 2. record provenance (sha256, size, URL, retrieval time)
python -m qad.research_tools.ma_enrollment.make_manifest [--fetch-log fetch_log.tsv]
# 3. compute (≈8 min first run; parsed inputs are cached in outputs/cache/)
python -m qad.research_tools.ma_enrollment.analysis
# 4. emit the five evidence-gap metrics
python -m qad.research_tools.ma_enrollment.emit_charter_metrics
# tests (synthetic only; no data needed)
python -m pytest -q tests/qad/research_tools
```
Run from the repository root.

## Definitions
- **MA universe:** organisation types Local CCP, Regional CCP, PFFS and MSA.
- **CPSC suppression:** cells with 10 or fewer members are blank. They are counted as 0 and measured against contract-file totals.
- **Repriced, "any":** any premium or MOOP increase, or a core supplemental (dental, eyewear, OTC) removed.
- **Repriced, "material":** premium up by at least $10 per month or from $0 to above $0, MOOP up by at least $500, or a supplemental removed.
- **Crosswalk components:** split and consolidated crosswalks are linked into connected components, and units are component × county.
