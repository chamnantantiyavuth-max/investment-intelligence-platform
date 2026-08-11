"""Shared Equity Universe — central equity universe layer (WP1, ChatGPT FIT-GAP).

Replaces per-strategy hard-coded ticker lists (e.g. FO_UNIVERSE in
discovery/equity_inflection/fetcher.py) with ONE deterministic, documented,
point-in-time identity layer that every discovery stream shares:

    Equity Universe
        ├── Equity Inflection (FD #88/#89)
        ├── Quality & Asymmetry Discovery (WP2)
        └── future discovery methods

Design rules (binding):
  - PIT identity (FD #58): every CIK/title pair is verified against SEC
    company_tickers.json (fetched 2026-08-11) and is valid as-of that date;
    re-verify before relying on it later.
  - Deterministic membership (FD #53): membership criteria are documented
    below, not AI-invented thresholds. No scoring, no weighting.
  - Advisory identity only: this layer answers "who is in scope + how do we
    identify them" — it NEVER makes investment judgments.
  - Portfolio-blind (Constitution §23.8.1): no portfolio context anywhere.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# ── Point-in-time stamp: source of truth for every CIK below ──
UNIVERSE_AS_OF = "2026-08-11"          # date CIKs were verified against SEC
UNIVERSE_SOURCE = "SEC company_tickers.json (https://www.sec.gov/files/company_tickers.json)"

# ── Membership criteria (documented, deterministic — FD #53) ──
# 1. US-listed common stocks / ADRs with SEC filings (companyfacts available).
# 2. FO-8 core (data-proven, FD #88/#89, FD #81 CIKs) — always included.
# 3. Large/mid-cap breadth: mega-caps + quality compounders + sector leaders
#    (consumer, financials, healthcare, industrials, tech, materials).
# 4. ADRs of major global issuers with US SEC filings (BABA, NVO, ASML, ...).
# 5. Every entry verified: ticker → CIK → title resolved from company_tickers.json.
# Re-verification: re-run `python -m discovery.equity_universe.verify` (or the
# ad-hoc verify in tests) against a fresh company_tickers.json before expanding.


@dataclass(frozen=True)
class EquityUniverseEntry:
    """One equity in the shared universe (immutable identity record)."""
    ticker: str
    cik: str                      # 10-digit zero-padded SEC CIK
    title: str                    # issuer name as reported to SEC
    sector: Optional[str] = None  # GICS-ish sector label (advisory, optional)
    is_adr: bool = False          # True for ADR listings (non-US domicile)

    @property
    def cik_int(self) -> int:
        return int(self.cik)


# ── The universe (98 names, CIKs verified 2026-08-11 from SEC) ──
_UNIVERSE: dict[str, EquityUniverseEntry] = {
    "AAPL": EquityUniverseEntry("AAPL", "0000320193", 'Apple Inc.'),
    "MSFT": EquityUniverseEntry("MSFT", "0000789019", 'MICROSOFT CORP'),
    "NVDA": EquityUniverseEntry("NVDA", "0001045810", 'NVIDIA CORP'),
    "GOOGL": EquityUniverseEntry("GOOGL", "0001652044", 'Alphabet Inc.'),
    "AMZN": EquityUniverseEntry("AMZN", "0001018724", 'AMAZON COM INC'),
    "META": EquityUniverseEntry("META", "0001326801", 'Meta Platforms, Inc.'),
    "TSLA": EquityUniverseEntry("TSLA", "0001318605", 'Tesla, Inc.'),
    "JNJ": EquityUniverseEntry("JNJ", "0000200406", 'JOHNSON & JOHNSON'),
    "BRK-B": EquityUniverseEntry("BRK-B", "0001067983", 'BERKSHIRE HATHAWAY INC'),
    "V": EquityUniverseEntry("V", "0001403161", 'VISA INC.'),
    "MA": EquityUniverseEntry("MA", "0001141391", 'MASTERCARD INC'),
    "JPM": EquityUniverseEntry("JPM", "0000019617", 'JPMORGAN CHASE & CO'),
    "UNH": EquityUniverseEntry("UNH", "0000731766", 'UNITEDHEALTH GROUP INC'),
    "XOM": EquityUniverseEntry("XOM", "0000034088", 'EXXON MOBIL CORP'),
    "LLY": EquityUniverseEntry("LLY", "0000059478", 'ELI LILLY & Co'),
    "AVGO": EquityUniverseEntry("AVGO", "0001730168", 'Broadcom Inc.'),
    "PG": EquityUniverseEntry("PG", "0000080424", 'PROCTER & GAMBLE Co'),
    "COST": EquityUniverseEntry("COST", "0000909832", 'COSTCO WHOLESALE CORP /NEW'),
    "WMT": EquityUniverseEntry("WMT", "0000104169", 'WALMART INC.'),
    "HD": EquityUniverseEntry("HD", "0000354950", 'HOME DEPOT, INC.'),
    "ABBV": EquityUniverseEntry("ABBV", "0001551152", 'ABBVIE INC.'),
    "KO": EquityUniverseEntry("KO", "0000021344", 'COCA-COLA CO'),
    "PEP": EquityUniverseEntry("PEP", "0000077476", 'PEPSICO INC'),
    "MCD": EquityUniverseEntry("MCD", "0000063908", 'MCDONALDS CORP'),
    "NKE": EquityUniverseEntry("NKE", "0000320187", 'NIKE, Inc.'),
    "DIS": EquityUniverseEntry("DIS", "0001744489", 'WALT DISNEY CO/'),
    "CSCO": EquityUniverseEntry("CSCO", "0000858877", 'CISCO SYSTEMS, INC.'),
    "ORCL": EquityUniverseEntry("ORCL", "0001341439", 'ORACLE CORP'),
    "CRM": EquityUniverseEntry("CRM", "0001108524", 'SALESFORCE, INC.'),
    "ACN": EquityUniverseEntry("ACN", "0001467373", 'ACCENTURE PLC'),
    "ADBE": EquityUniverseEntry("ADBE", "0000796343", 'ADOBE INC.'),
    "TXN": EquityUniverseEntry("TXN", "0000097476", 'TEXAS INSTRUMENTS INC'),
    "QCOM": EquityUniverseEntry("QCOM", "0000804328", 'QUALCOMM INC/DE'),
    "INTU": EquityUniverseEntry("INTU", "0000896878", 'INTUIT INC.'),
    "AMGN": EquityUniverseEntry("AMGN", "0000318154", 'AMGEN INC'),
    "GILD": EquityUniverseEntry("GILD", "0000882095", 'GILEAD SCIENCES, INC.'),
    "TMO": EquityUniverseEntry("TMO", "0000097732", 'THERMO FISHER SCIENTIFIC INC.'),
    "ABT": EquityUniverseEntry("ABT", "0000001800", 'ABBOTT LABORATORIES'),
    "SBUX": EquityUniverseEntry("SBUX", "0000829224", 'STARBUCKS CORP'),
    "LOW": EquityUniverseEntry("LOW", "0000060667", "LOWE'S COMPANIES INC"),
    "MDLZ": EquityUniverseEntry("MDLZ", "0001103982", 'Mondelez International, Inc.'),
    "CVS": EquityUniverseEntry("CVS", "0000064803", 'CVS HEALTH Corp'),
    "PFE": EquityUniverseEntry("PFE", "0000078003", 'PFIZER INC'),
    "MRK": EquityUniverseEntry("MRK", "0000310158", 'MERCK & CO., INC.'),
    "BMY": EquityUniverseEntry("BMY", "0000014272", 'BRISTOL-MYERS SQUIBB CO'),
    "CAT": EquityUniverseEntry("CAT", "0000018230", 'CATERPILLAR INC'),
    "DE": EquityUniverseEntry("DE", "0000031518", 'DEERE & CO'),
    "HON": EquityUniverseEntry("HON", "0000773840", 'HONEYWELL INTERNATIONAL INC'),
    "LIN": EquityUniverseEntry("LIN", "0001707925", 'LINDE PLC'),
    "SHW": EquityUniverseEntry("SHW", "0000089800", 'SHERWIN-WILLIAMS CO'),
    "MRSH": EquityUniverseEntry("MRSH", "0000062709", 'MARSH & MCLENNAN COMPANIES, INC.'),
    "SPGI": EquityUniverseEntry("SPGI", "0000064040", 'S&P GLOBAL INC.'),
    "MCO": EquityUniverseEntry("MCO", "0001059556", 'MOODYS CORP /DE/'),
    "BLK": EquityUniverseEntry("BLK", "0001364742", 'BlackRock, Inc.'),
    "GS": EquityUniverseEntry("GS", "0000886982", 'GOLDMAN SACHS GROUP INC'),
    "MS": EquityUniverseEntry("MS", "0000895421", 'MORGAN STANLEY'),
    "BAC": EquityUniverseEntry("BAC", "0000070858", 'BANK OF AMERICA CORP /DE/'),
    "WFC": EquityUniverseEntry("WFC", "0000101777", 'WELLS FARGO & CO/MN'),
    "UBER": EquityUniverseEntry("UBER", "0001543151", 'Uber Technologies, Inc.'),
    "SHOP": EquityUniverseEntry("SHOP", "0001561552", 'SHOPIFY INC.'),
    "PLTR": EquityUniverseEntry("PLTR", "0001321655", 'Palantir Technologies Inc.'),
    "SNOW": EquityUniverseEntry("SNOW", "0001640147", 'Snowflake Inc.'),
    "NET": EquityUniverseEntry("NET", "0001475430", 'Cloudflare, Inc.'),
    "DDOG": EquityUniverseEntry("DDOG", "0001567890", 'DATADOG, INC.'),
    "CRWD": EquityUniverseEntry("CRWD", "0001535527", 'CrowdStrike Holdings, Inc.'),
    "PANW": EquityUniverseEntry("PANW", "0001327567", 'Palo Alto Networks Inc.'),
    "NOW": EquityUniverseEntry("NOW", "0001373715", 'ServiceNow, Inc.'),
    "VRTX": EquityUniverseEntry("VRTX", "0000875320", 'VERTEX PHARMACEUTICALS INC / MA'),
    "SYK": EquityUniverseEntry("SYK", "0000310764", 'STRYKER CORP'),
    "ISRG": EquityUniverseEntry("ISRG", "0001035267", 'INTUITIVE SURGICAL INC'),
    "EW": EquityUniverseEntry("EW", "0001099800", 'Edwards Lifesciences Corp'),
    "BSX": EquityUniverseEntry("BSX", "0000885725", 'BOSTON SCIENTIFIC CORP'),
    "DXCM": EquityUniverseEntry("DXCM", "0001093557", 'DEXCOM INC'),
    "MELI": EquityUniverseEntry("MELI", "0001099590", 'MERCADOLIBRE INC'),
    "ADSK": EquityUniverseEntry("ADSK", "0000769397", 'AUTODESK, INC.'),
    "ROP": EquityUniverseEntry("ROP", "0000882394", 'ROPER TECHNOLOGIES INC'),
    "FTNT": EquityUniverseEntry("FTNT", "0001262039", 'FORTINET, INC.'),
    "ZM": EquityUniverseEntry("ZM", "0001585521", 'Zoom Video Communications, Inc.'),
    "BABA": EquityUniverseEntry("BABA", "0001577552", 'Alibaba Group Holding Ltd', is_adr=True),
    "PDD": EquityUniverseEntry("PDD", "0001737806", 'Pinduoduo Inc.', is_adr=True),
    "NVO": EquityUniverseEntry("NVO", "0000353018", 'NOVO NORDISK A/S', is_adr=True),
    "ASML": EquityUniverseEntry("ASML", "0000937966", 'ASML HOLDING NV', is_adr=True),
    "TM": EquityUniverseEntry("TM", "0001094517", 'TOYOTA MOTOR CORP/', is_adr=True),
    "SONY": EquityUniverseEntry("SONY", "0000313838", 'SONY GROUP CORP', is_adr=True),
    "HDB": EquityUniverseEntry("HDB", "0001144967", 'HDFC BANK LTD', is_adr=True),
    "INFY": EquityUniverseEntry("INFY", "0001067491", 'INFOSYS LTD', is_adr=True),
    "TSM": EquityUniverseEntry("TSM", "0001046179", 'TAIWAN SEMICONDUCTOR MANUFACTURING CO LTD', is_adr=True),
    "UL": EquityUniverseEntry("UL", "0000351038", 'UNILEVER PLC', is_adr=True),
    "AZN": EquityUniverseEntry("AZN", "0000901837", 'ASTRAZENECA PLC', is_adr=True),
    "SNY": EquityUniverseEntry("SNY", "0001121404", 'SANOFI', is_adr=True),
    "NVS": EquityUniverseEntry("NVS", "0000100039", 'NOVARTIS AG', is_adr=True),
    "BP": EquityUniverseEntry("BP", "0000313807", 'BP PLC', is_adr=True),
    "SHEL": EquityUniverseEntry("SHEL", "0001306965", 'SHELL PLC', is_adr=True),
    "TMUS": EquityUniverseEntry("TMUS", "0001283699", 'T-MOBILE US, INC.'),
    "SAP": EquityUniverseEntry("SAP", "0001001114", 'SAP SE', is_adr=True),
    "VOD": EquityUniverseEntry("VOD", "0000839923", 'VODAFONE GROUP PUBLIC LTD CO', is_adr=True),
    "RIO": EquityUniverseEntry("RIO", "0000863064", 'RIO TINTO PLC', is_adr=True),
    "BHP": EquityUniverseEntry("BHP", "0000811809", 'BHP GROUP LTD', is_adr=True),
}


def get_universe() -> dict[str, EquityUniverseEntry]:
    """Return the full universe (ticker → entry). Deterministic, no side effects."""
    return dict(_UNIVERSE)


def get_tickers() -> list[str]:
    """Ordered ticker list (insertion order = curated order)."""
    return list(_UNIVERSE.keys())


def get_entry(ticker: str) -> EquityUniverseEntry:
    """Resolve one ticker. Raises KeyError if not in universe."""
    return _UNIVERSE[ticker]


def get_cik(ticker: str) -> str:
    """Resolve the 10-digit CIK for a ticker (KeyError if unknown)."""
    return _UNIVERSE[ticker].cik


def is_in_universe(ticker: str) -> bool:
    return ticker in _UNIVERSE


def get_by_cik(cik: str) -> Optional[EquityUniverseEntry]:
    """Reverse lookup CIK → entry (None if not present)."""
    for e in _UNIVERSE.values():
        if e.cik == cik:
            return e
    return None


# ── Backward compatibility: FO-8 subset (FD #81 verified CIKs) ──
FO8_TICKERS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "JNJ"]

def get_fo8() -> dict[str, EquityUniverseEntry]:
    """FO-8 core subset (data-proven, FD #88/#89 pipeline)."""
    return {t: _UNIVERSE[t] for t in FO8_TICKERS}
