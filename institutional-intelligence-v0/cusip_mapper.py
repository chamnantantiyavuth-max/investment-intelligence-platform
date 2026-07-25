"""
Institutional Intelligence V0 — Ticker Mapper
Maps issuer names from 13F filings to standard tickers.
Simple lookup table — expandable.

Phase 10.5 · FD #42 · 26 July 2026
"""

# Known mappings: issuer name substring → ticker
NAME_TO_TICKER = {
    "APPLE INC": "AAPL",
    "MICROSOFT CORP": "MSFT",
    "NVIDIA CORP": "NVDA",
    "ALPHABET INC": "GOOGL",
    "AMAZON COM INC": "AMZN",
    "META PLATFORMS": "META",
    "TESLA INC": "TSLA",
    "BERKSHIRE HATHAWAY": "BRK.B",
    "JOHNSON & JOHNSON": "JNJ",
    "JPMORGAN CHASE": "JPM",
    "VISA INC": "V",
    "UNITEDHEALTH GROUP": "UNH",
    "WALMART INC": "WMT",
    "EXXON MOBIL": "XOM",
    "BANK OF AMERICA": "BAC",
    "PROCTER & GAMBLE": "PG",
    "COSTCO WHOLESALE": "COST",
    "MASTERCARD INC": "MA",
    "HOME DEPOT": "HD",
    "CHEVRON CORP": "CVX",
    "ABBVIE INC": "ABBV",
    "PEPSICO INC": "PEP",
    "COCA COLA": "KO",
    "MERCK & CO": "MRK",
    "BROADCOM INC": "AVGO",
    "ADOBE INC": "ADBE",
    "SALESFORCE INC": "CRM",
    "ORACLE CORP": "ORCL",
    "CISCO SYSTEMS": "CSCO",
    "NETFLIX INC": "NFLX",
    "ADVANCED MICRO DEVICES": "AMD",
    "INTEL CORP": "INTC",
    "QUALCOMM INC": "QCOM",
    "TEXAS INSTRUMENTS": "TXN",
    "INTUIT INC": "INTU",
    "UBER TECHNOLOGIES": "UBER",
    "PALO ALTO NETWORKS": "PANW",
    "CROWDSTRIKE HLDGS": "CRWD",
    "SNOWFLAKE INC": "SNOW",
    "SERVICENOW INC": "NOW",
    "SHOPIFY INC": "SHOP",
    "STRYKER CORP": "SYK",
    "NIKE INC": "NKE",
    "STARBUCKS CORP": "SBUX",
    "DISNEY WALT": "DIS",
    "GENERAL ELECTRIC": "GE",
    "BOEING CO": "BA",
    "CATERPILLAR INC": "CAT",
    "GOLDMAN SACHS": "GS",
    "MORGAN STANLEY": "MS",
    "AMERICAN EXPRESS": "AXP",
    "OCCIDENTAL PETE": "OXY",
    "CITIGROUP INC": "C",
    "LILLY ELI": "LLY",
    "PFIZER INC": "PFE",
    "CHIPOTLE MEXICAN": "CMG",
    "HILTON WORLDWIDE": "HLT",
    "RESTAURANT BRANDS": "QSR",
    "LOWES COMPANIES": "LOW",
    "JD COM INC": "JD",
    "ALIBABA GROUP": "BABA",
    "GEO GROUP INC": "GEO",
    "CORECIVIC INC": "CXW",
    "ROCKET COS INC": "RKT",
    "NU HLDGS LTD": "NU",
    "DATADOG INC": "DDOG",
    "AMAZON COM": "AMZN",
    "UBER": "UBER",
    # Berkshire 13F specific
    "BANK AMER CORP": "BAC",
    "AMERICAN EXPRESS CO": "AXP",
    "COCA COLA CO": "KO",
    "CHEVRON CORP NEW": "CVX",
    "OCCIDENTAL PETE CORP": "OXY",
    "MOODYS CORP": "MCO",
    "KRAFT HEINZ CO": "KHC",
    "DAVITA INC": "DVA",
    "CHARTER COMMUNICATIONS": "CHTR",
    "LIBERTY MEDIA CORP": "LSXMA",
    "SIRIUS XM HLDGS INC": "SIRI",
    "VERISIGN INC": "VRSN",
    "FLOOR & DECOR HLDGS": "FND",
    "LENNAR CORP": "LEN",
    "DR HORTON INC": "DHI",
    "NVR INC": "NVR",
    "CAPITAL ONE FINL CORP": "COF",
    "MASTERCARD INCORPORATED": "MA",
    "VISA INC": "V",
    "AMAZON COM INC": "AMZN",
    "ALLSTATE CORP": "ALL",
    "T-MOBILE US INC": "TMUS",
    "LOUISIANA PAC CORP": "LPX",
    "POOL CORP": "POOL",
    "DIAGEO PLC": "DEO",
    "BYD CO LTD": "BYDDY",
    "MITSUBISHI CORP": "MSBHF",
    "MITSUI & CO LTD": "MITSY",
    "ITOCHU CORP": "ITOCY",
    "MARUBENI CORP": "MARUY",
    "SUMITOMO CORP": "SSUMY",
}


def name_to_ticker(name: str) -> str | None:
    """Fuzzy match issuer name → ticker."""
    name_upper = name.upper().strip()
    # Direct match
    if name_upper in NAME_TO_TICKER:
        return NAME_TO_TICKER[name_upper]
    # Substring match
    for key, ticker in NAME_TO_TICKER.items():
        if key in name_upper or name_upper in key:
            return ticker
    return None


def enrich_holdings(holdings: list[dict]) -> list[dict]:
    """Add ticker field to holdings, derived from issuer name."""
    for h in holdings:
        h["ticker"] = name_to_ticker(h.get("name", "")) or h.get("cusip", "UNKNOWN")
    return holdings
