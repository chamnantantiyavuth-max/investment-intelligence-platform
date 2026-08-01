"""
Institutional Intelligence V0 — SEC EDGAR 13F Fetcher
Real 13F data from SEC EDGAR. Parses XML → normalized holdings.

Phase 10.5 · FD #42 · 26 July 2026
"""

import json
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
USER_AGENT = "IIP-Research/1.0 (admin@iip.local)"

# SEC rate limit: 10 requests/second
REQUEST_DELAY = 0.15  # seconds between requests


def _cache_path(cik: str, quarter: str) -> Path:
    return CACHE_DIR / f"{cik}_{quarter}.json"


def _load_cache(cik: str, quarter: str, max_age_hours: int = 24) -> dict | None:
    path = _cache_path(cik, quarter)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    fetched = datetime.fromisoformat(data.get("_fetched_at", "2000-01-01"))
    age = (datetime.now() - fetched).total_seconds() / 3600
    if age > max_age_hours:
        return None
    return data


def _save_cache(cik: str, quarter: str, data: dict):
    data["_fetched_at"] = datetime.now().isoformat()
    _cache_path(cik, quarter).write_text(
        json.dumps(data, indent=2, default=str), encoding="utf-8"
    )


def _sec_get(url: str, timeout: int = 30) -> str:
    """GET request to SEC EDGAR with rate limiting."""
    time.sleep(REQUEST_DELAY)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def find_latest_13f(cik: str) -> dict | None:
    """Find the latest 13F-HR filing accession for a CIK.

    Returns: {"accession": "...", "report_date": "2026-03-31", "cik": "..."}
    """
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    try:
        data = json.loads(_sec_get(url))
    except Exception as e:
        print(f"  [WARN] SEC API failed for {cik}: {e}")
        return None

    filings = data.get("filings", {}).get("recent", {})
    forms = filings.get("form", [])
    for i, form in enumerate(forms):
        if form == "13F-HR":
            return {
                "cik": cik,
                "accession": filings["accessionNumber"][i],
                "report_date": filings["reportDate"][i],
                "filing_date": filings.get("filingDate", [None])[i],
            }
    return None


def download_13f_holdings(filing: dict) -> list[dict]:
    """Download and parse a 13F filing's information table.

    Args:
        filing: {"cik": "0001067983", "accession": "0001193125-26-226661", ...}

    Returns:
        List of holding dicts: {"name": "APPLE INC", "cusip": "037833100", "value_usd": ..., "shares": ...}
    """
    cik_num = filing["cik"].lstrip("0")
    acc = filing["accession"]
    acc_clean = acc.replace("-", "")

    # Step 1: Get filing index page to find the information table XML
    index_url = f"https://www.sec.gov/Archives/edgar/data/{cik_num}/{acc_clean}/{acc}-index.htm"
    try:
        index_html = _sec_get(index_url)
    except Exception as e:
        print(f"  [WARN] Failed to get filing index for {filing['cik']}: {e}")
        return []

    # Find XML file links
    xml_files = re.findall(r'href="([^"]+\.xml)"', index_html)
    # The information table is typically named like '12345.xml' (not primary_doc.xml)
    info_table_url = None
    for xf in xml_files:
        basename = xf.split("/")[-1]
        # Skip primary_doc.xml and xslForm files
        if basename == "primary_doc.xml" or "xslForm" in xf:
            continue
        if basename.endswith(".xml"):
            info_table_url = f"https://www.sec.gov{xf}"
            break

    if not info_table_url:
        # Fallback: try primary_doc.xml
        for xf in xml_files:
            if xf.endswith("primary_doc.xml"):
                info_table_url = f"https://www.sec.gov{xf}"
                break

    if not info_table_url:
        print(f"  [WARN] No information table found for {filing['cik']}")
        return []

    # Step 2: Download and parse the information table XML
    try:
        xml_text = _sec_get(info_table_url, timeout=60)
    except Exception as e:
        print(f"  [WARN] Failed to download XML for {filing['cik']}: {e}")
        return []

    return _parse_13f_xml(xml_text)


def _parse_13f_xml(xml_text: str) -> list[dict]:
    """Parse 13F information table XML → list of holding dicts.

    Aggregates duplicate CUSIP entries (13F reports by manager).
    """
    # Remove encoding declaration if it causes issues
    xml_text = re.sub(r'<\?xml[^?]*\?>', '', xml_text)

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        # Try cleaning up common XML issues
        xml_text = xml_text.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
        root = ET.fromstring(xml_text)

    NS = "http://www.sec.gov/edgar/document/thirteenf/informationtable"

    # Aggregate by CUSIP (handle multiple managers reporting same position)
    holdings_by_cusip: dict[str, dict] = {}
    total_value = 0

    for it in root.iter(f"{{{NS}}}infoTable"):
        name_el = it.find(f"{{{NS}}}nameOfIssuer")
        cusip_el = it.find(f"{{{NS}}}cusip")
        value_el = it.find(f"{{{NS}}}value")
        shrs_el = it.find(f"{{{NS}}}shrsOrPrnAmt/{{{NS}}}sshPrnamt")
        typ_el = it.find(f"{{{NS}}}shrsOrPrnAmt/{{{NS}}}sshPrnamtType")

        if cusip_el is None or value_el is None:
            continue

        cusip = cusip_el.text.strip()
        name = name_el.text.strip() if name_el is not None else "Unknown"
        # Value is in THOUSANDS of dollars
        value_thousands = int(value_el.text.strip())
        shares = int(shrs_el.text.strip()) if shrs_el is not None else 0

        if cusip in holdings_by_cusip:
            holdings_by_cusip[cusip]["value_usd"] += value_thousands * 1000
            holdings_by_cusip[cusip]["shares"] += shares
        else:
            holdings_by_cusip[cusip] = {
                "name": name,
                "cusip": cusip,
                "value_usd": value_thousands * 1000,
                "shares": shares,
            }
        total_value += value_thousands * 1000

    # Convert to list + add pct_of_portfolio
    holdings = []
    for h in holdings_by_cusip.values():
        h["pct_of_portfolio"] = round(h["value_usd"] / total_value * 100, 2) if total_value > 0 else 0
        holdings.append(h)

    # Sort by value descending
    holdings.sort(key=lambda x: x["value_usd"], reverse=True)
    return holdings


def fetch_fund_13f(cik: str, force_refresh: bool = False) -> dict | None:
    """Fetch latest 13F for a fund CIK — with caching.

    Returns a filing dict compatible with pipeline FIXTURES format:
        {
            "filer_name": "Berkshire Hathaway",
            "filer_cik": "0001067983",
            "filing_quarter": "2026Q1",
            "report_date": "2026-03-31",
            "total_value_usd": 672_000_000_000,
            "total_positions": 41,
            "holdings": [{name, cusip, value_usd, shares, pct_of_portfolio}, ...]
        }
    """
    # Check cache first
    if not force_refresh:
        # Find latest cached quarter for this CIK
        cached = None
        for f in sorted(CACHE_DIR.glob(f"{cik}_*.json"), reverse=True):
            cached = _load_cache(cik, f.stem.split("_", 1)[1])
            if cached:
                break
        if cached:
            return cached

    # Find latest filing
    filing_info = find_latest_13f(cik)
    if not filing_info:
        return None

    print(f"  Downloading {filing_info['report_date']} for {cik}...")

    # Download and parse
    holdings = download_13f_holdings(filing_info)
    if not holdings:
        return None

    # Convert report_date to quarter string
    rd = filing_info["report_date"]
    q = _date_to_quarter(rd)

    total_value = sum(h["value_usd"] for h in holdings)

    # Get filer name from watchlist
    from watchlist import get_fund
    fund = get_fund(cik=cik)
    filer_name = fund["name"] if fund else cik

    result = {
        "filer_name": filer_name,
        "filer_cik": cik,
        "filing_quarter": q,
        "report_date": rd,
        "filing_date": filing_info.get("filing_date", ""),
        "accession": filing_info["accession"],
        "total_value_usd": total_value,
        "total_positions": len(holdings),
        "holdings": holdings,
        "source": "SEC EDGAR",
        "fixture_category": "REAL 13F — SEC EDGAR — FOR V0 DEVELOPMENT ONLY",
    }

    _save_cache(cik, q, result)
    return result


def fetch_all_watchlist(force_refresh: bool = False, max_funds: int = None) -> list[dict]:
    """Fetch latest 13F for all watchlist funds.

    Args:
        force_refresh: Ignore cache and re-fetch.
        max_funds: Limit to first N funds (for testing).

    Returns:
        List of filing dicts compatible with pipeline.
    """
    from watchlist import get_all_ciks
    ciks = get_all_ciks()
    if max_funds:
        ciks = ciks[:max_funds]

    results = []
    attempted = 0
    failed = 0
    for i, cik in enumerate(ciks):
        attempted += 1
        print(f"[{i+1}/{len(ciks)}] {cik}", end=" ")
        try:
            filing = fetch_fund_13f(cik, force_refresh=force_refresh)
            if filing:
                results.append(filing)
                print(f"→ {filing['total_positions']} holdings, ${filing['total_value_usd']/1e9:.0f}B")
            else:
                failed += 1
                print("→ No 13F found")
        except Exception as e:
            failed += 1
            print(f"→ Error: {e}")

    if failed:
        print(
            f"\n⚠️  INCOMPLETE FETCH: {attempted - failed}/{attempted} funds succeeded, "
            f"{failed} failed or missing. Output is NOT authoritative as a full watchlist run."
        )

    return {
        "filings": results,
        "summary": {
            "attempted": attempted,
            "succeeded": len(results),
            "failed": failed,
            "complete": failed == 0,
        },
    }


def _date_to_quarter(date_str: str) -> str:
    """Convert '2026-03-31' → '2026Q1'."""
    dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}Q{q}"
