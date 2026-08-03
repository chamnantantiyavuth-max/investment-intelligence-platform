# Final Browser Lane — Real-Data Production Path (FD #46)

> Date: 2026-08-03 · Operator: Parent (browser tools — subagents cannot operate the browser)
> App: localhost:5173 (vite) → :8000 (uvicorn, auth env set) · Verdict input for Final Council

## Workflows exercised (BROWSER_VERIFIED)

| # | Workflow | Result | Evidence |
|---|----------|--------|----------|
| 1 | Login gate renders when unauthenticated | ✅ | LoginPage visible, no app data leaked |
| 2 | Wrong-password → login failure path | ✅ (API-verified 401) | curl wrong password → 401 |
| 3 | Correct login → dashboard | ✅ | auth/status true; dashboard renders |
| 4 | Dashboard per-component provenance | ✅ | AM `real_yahoo_finance_eod`, FO `real_yfinance`, II real, CS `synthetic_demo` labels visible |
| 5 | Dashboard CS triple agreement (SOL-003) | ✅ | dashboard 2/1 == /api/cs-radar 2 assets/1 Q-met == mock source oracle (2,1) |
| 6 | AM queue real data | ✅ | 5 themes (Medical Devices, Cloud Infra, Cybersecurity, Semiconductors, Solar), run AM-V0-20260803-171535, hybrid banner |
| 7 | AM theme detail + evidence provenance | ✅ | TH-014 {theme, candidates}; badges EV-007·synthetic, EV-008·synthetic, EV-009·human_sourced, EV-FK-002·human_sourced |
| 8 | FO queue real data | ✅ | 8 companies (AAPL..JNJ), "REAL · yfinance" badge, NOT_TRIGGERED verdicts |
| 9 | CS radar synthetic label | ✅ | "SYNTHETIC / DEMO — NOT LIVE DATA", 2 assets (BRK.B 4/5, JNJ 5/5) |
| 10 | JS error sweep | ✅ | 0 JS errors across all pages (only pre-existing Base UI a11y advisories) |

## Evidence

- Screenshots: `C:\Users\Admin\AppData\Local\hermes\profiles\iip\cache\screenshots\browser_screenshot_da8e23fcd73a49e3913faad9da0b40b0.png` (AM theme evidence provenance)
- API captures: all endpoints 200 with real data (see Final Council API/oracle lane section)
- Console: 0 errors

## Notes

- II surface (25,246 signals) verified at API level; no dedicated II page in nav (out of FD #46 scope — API surface only).
- Base UI button-advisory console messages are pre-existing shadcn/ui accessibility warnings, not defects.

<!-- 2026-08-03 21:32 UTC+7 -->
