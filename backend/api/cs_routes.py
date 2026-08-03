"""Close System API routes."""
from fastapi import APIRouter, Depends

from backend.auth import require_auth

router = APIRouter(prefix="/api", tags=["close-system"], dependencies=[Depends(require_auth)])

# DEMO DATA — static demonstration assets, NOT live pipeline output.
# data_source field on the response marks this provenance (Constitution §8/§23.4).
_MOCK_ASSETS = [
    {
        "ticker": "BRK.B", "name": "Berkshire Hathaway", "sector": "Financials",
        "q_conditions_met": 4, "q_conditions_total": 5,
        "q_details": [
            {"name": "Earnings Stability", "met": True, "value": "15yr positive"},
            {"name": "Dividend Record", "met": True, "value": "No dividend"},
            {"name": "Earnings Growth", "met": True, "value": "12% 10yr CAGR"},
            {"name": "P/E Moderate", "met": True, "value": "P/E 14.2"},
            {"name": "Price/Book", "met": False, "value": "P/B 1.6x (>1.5x)"},
        ],
        "dimensions": {
            "suitability": 8.0, "opportunity": 5.5, "regime": "compatible",
            "decay": "low", "data_confidence": 8.5,
        },
        "rule_pack": ["graham_value"], "instrument": "common_stock",
        "liquidity": "1.2B", "capital_lockup": "none",
    },
    {
        "ticker": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare",
        "q_conditions_met": 5, "q_conditions_total": 5,
        "q_details": [
            {"name": "Earnings Stability", "met": True, "value": "20yr positive"},
            {"name": "Dividend Record", "met": True, "value": "62yr growth"},
            {"name": "Earnings Growth", "met": True, "value": "6% 10yr CAGR"},
            {"name": "P/E Moderate", "met": True, "value": "P/E 16.1"},
            {"name": "Price/Book", "met": True, "value": "P/B 5.2x"},
        ],
        "dimensions": {
            "suitability": 9.0, "opportunity": 7.0, "regime": "compatible",
            "decay": "low", "data_confidence": 9.0,
        },
        "rule_pack": ["graham_value", "dividend_aristocrat"],
        "instrument": "common_stock", "liquidity": "3.5B", "capital_lockup": "none",
    },
]


@router.get("/cs-radar")
async def get_cs_radar():
    return {"data_source": "synthetic_demo", "assets": _MOCK_ASSETS}
