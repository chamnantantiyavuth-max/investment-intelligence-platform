# Industry Outlook — Reference Layer

> **Purpose:** Structured "where to look" notes per industry, extracted from the Investopedia Industry Handbook series in `docs/Books/` (static PDFs, gitignored). These notes are research-direction references — they tell us what to measure, who sits where in the supply chain, and where to find current data.

## ⚠️ FD #58 — Point-in-Time Data Rule (Must Rule)

All quantitative figures in these notes were extracted from reference works written in **2015** (Investopedia handbooks) or earlier.

- **Every number is a historical value, valid only at the source's publication date. It MUST NOT be treated as current.**
- Before any figure here informs a theme, candidate, evidence, or pipeline output, it must be **updated or re-verified against a current source** (company filings, live market data, current industry statistics).
- The durable value of these notes is **structural and conceptual**: supply-chain structure, what to measure, where to look, Porter's 5 Forces, valuation frameworks. **The numbers expire; the frameworks do not.**
- Encoding: `operational/EVIDENCE-DOCTRINE.md` (Aging → Point-in-Time Data in Reference Works) + `operational/FOUNDERS-DECISIONS.md` FD #58.

## Note Format

Each industry note follows the same skeleton:

| Section | Content | Durable? |
|---|---|---|
| Source | Handbook name + publication year | — |
| Supply chain | Who sits where; segment structure | ✅ durable |
| What to measure | Key ratios/terms + what they signal | ✅ durable (numbers flagged ⚠️) |
| Where to look | Data sources, publications, filings | ✅ durable (verify still live) |
| Analyst insight | Framework for reading the industry | ✅ durable |
| Porter's 5 Forces | New entrants / suppliers / buyers / substitutes / rivalry | ✅ durable |
| Direct commodity investment | Investing in the commodity itself (physical, ETFs, futures, options) vs the companies | ✅ durable (tickers/specs ⚠️ verify current) |
| Theme mapping | Controlled Theme IDs this industry feeds | — |

Numbers from the handbook are marked **[2015]** inline. Anything needing a current figure carries a **TODO-UPDATE** marker.

**Direct Commodity Investment section — commodity-only rule:** appears ONLY in notes for industries with a directly-traded underlying commodity (precious metals, oil/energy, agriculture). Omitted entirely from all other industry notes — no placeholder, no "vehicle unavailable" filler. Of the 7 handbooks: Precious Metals ✅ (done), Oil Services ✅ (gets it), the other 5 (Utilities, Telecom, Semiconductor, Internet, Biotechnology) ❌ (no directly-traded commodity).

## Index

| Industry | Note | Direct Commodity Section | Controlled Themes |
|---|---|---|---|
| Precious Metals | [PRECIOUS-METALS.md](PRECIOUS-METALS.md) | ✅ | TH-115 Gold, TH-116 Other Precious Metals & Mining, TH-122 Silver |
| Semiconductors | [SEMICONDUCTOR.md](SEMICONDUCTOR.md) | ❌ | TH-004 Semiconductors, TH-009 Semiconductor Equipment & Materials |
| Oil Services | [OIL-SERVICES.md](OIL-SERVICES.md) | ✅ | TH-107/TH-111 (Equip & Services / Drilling), TH-105/108/109 (E&P / Integrated / Refining) |
| Biotechnology | [BIOTECHNOLOGY.md](BIOTECHNOLOGY.md) | ❌ | TH-013 Biotechnology, TH-015 Drug Specialty, TH-020 Drug General |
| Internet | [INTERNET.md](INTERNET.md) | ❌ | TH-038 Internet Content & Information |
| Telecommunications | [TELECOMMUNICATIONS.md](TELECOMMUNICATIONS.md) | ❌ | TH-039 Telecom Services |
| Utilities | [UTILITIES.md](UTILITIES.md) | ❌ | TH-139–144 (Regulated Electric/Gas/Water, Renewable, IPP, Diversified) |

*Status: all 7 handbooks extracted (5 Aug 2026).*
<!-- 2026-08-05 23:55 UTC+7 -->
