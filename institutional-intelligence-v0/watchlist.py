"""
Institutional Intelligence V0 — Super-Investor Watchlist
Curated registry of high-signal institutional investors.
Categories: Legendary, Tiger Cubs, Major Funds, Activists, Sector Specialists.

FD #42 · Phase 10 · 26 July 2026
"""

WATCHLIST = [
    # ── 🏆 Legendary Investors ──
    {"name": "Berkshire Hathaway",       "cik": "0001067983", "manager": "Warren Buffett",          "category": "Legendary", "style": "Value/Quality",      "aum_b": 672},
    {"name": "Scion Asset Management",   "cik": "0001649339", "manager": "Michael Burry",           "category": "Legendary", "style": "Deep Value/Macro",    "aum_b": 0.2},
    {"name": "Bridgewater Associates",   "cik": "0001350694", "manager": "Ray Dalio",               "category": "Legendary", "style": "Global Macro",         "aum_b": 124},
    {"name": "Baupost Group",            "cik": "0001061768", "manager": "Seth Klarman",             "category": "Legendary", "style": "Deep Value/Distressed","aum_b": 27},
    {"name": "Pershing Square Capital",  "cik": "0001336528", "manager": "Bill Ackman",              "category": "Legendary", "style": "Activist/Concentrated", "aum_b": 16},
    {"name": "Greenlight Capital",       "cik": "0001079114", "manager": "David Einhorn",            "category": "Legendary", "style": "Long-Short Value",     "aum_b": 2},
    {"name": "Paulson & Co.",            "cik": "0001338470", "manager": "John Paulson",             "category": "Legendary", "style": "Event-Driven/Macro",   "aum_b": 5},
    {"name": "Appaloosa Management",     "cik": "0001035674", "manager": "David Tepper",             "category": "Legendary", "style": "Distressed/Macro",     "aum_b": 14},
    {"name": "Elliott Management",       "cik": "0001048122", "manager": "Paul Singer",              "category": "Legendary", "style": "Activist/Distressed",  "aum_b": 59},
    {"name": "Third Point",              "cik": "0001040273", "manager": "Dan Loeb",                 "category": "Legendary", "style": "Activist/Event-Driven","aum_b": 11},
    {"name": "Duquesne Family Office",   "cik": "0001539633", "manager": "Stanley Druckenmiller",    "category": "Legendary", "style": "Macro/Growth",          "aum_b": 4},
    {"name": "Renaissance Technologies", "cik": "0001037389", "manager": "Jim Simons (estate)",      "category": "Legendary", "style": "Quant/Systematic",      "aum_b": 65},

    # ── 🐅 Tiger Cubs (Julian Robertson protégés) ──
    {"name": "Tiger Global Management",  "cik": "0001167483", "manager": "Chase Coleman",             "category": "Tiger Cub",  "style": "Growth/Tech",          "aum_b": 52},
    {"name": "Viking Global Investors",  "cik": "0001103804", "manager": "Andreas Halvorsen",         "category": "Tiger Cub",  "style": "Growth/Concentrated",  "aum_b": 30},
    {"name": "Maverick Capital",         "cik": "0000902724", "manager": "Lee Ainslie",               "category": "Tiger Cub",  "style": "Long-Short Growth",    "aum_b": 8},
    {"name": "Lone Pine Capital",        "cik": "0001061165", "manager": "Stephen Mandel",            "category": "Tiger Cub",  "style": "Growth/Concentrated",  "aum_b": 15},
    {"name": "Coatue Management",        "cik": "0001137050", "manager": "Philippe Laffont",          "category": "Tiger Cub",  "style": "Tech/Growth",          "aum_b": 45},
    {"name": "D1 Capital Partners",      "cik": "0001748824", "manager": "Daniel Sundheim",           "category": "Tiger Cub",  "style": "Growth/Concentrated",  "aum_b": 20},
    {"name": "Hound Partners",           "cik": "0001541617", "manager": "Jonathan Auerbach",         "category": "Tiger Cub",  "style": "Long-Short Growth",    "aum_b": 3},

    # ── 🏦 Major Multi-Strategy Funds ──
    {"name": "Citadel Advisors",         "cik": "0001423053", "manager": "Ken Griffin",               "category": "Major Fund", "style": "Multi-Strategy",       "aum_b": 63},
    {"name": "Millennium Management",    "cik": "0001273087", "manager": "Izzy Englander",            "category": "Major Fund", "style": "Multi-Strategy",       "aum_b": 62},
    {"name": "Point72 Asset Management", "cik": "0001603466", "manager": "Steve Cohen",               "category": "Major Fund", "style": "Multi-Strategy",       "aum_b": 34},
    {"name": "DE Shaw & Co.",            "cik": "0001009207", "manager": "David Shaw",                "category": "Major Fund", "style": "Quant/Systematic",      "aum_b": 60},
    {"name": "Two Sigma Investments",    "cik": "0001179392", "manager": "John Overdeck/David Siegel","category": "Major Fund", "style": "Quant/Systematic",      "aum_b": 58},
    {"name": "Balyasny Asset Management","cik": "0001398348", "manager": "Dmitry Balyasny",           "category": "Major Fund", "style": "Multi-Strategy",       "aum_b": 21},
    {"name": "Marshall Wace",            "cik": "0001315452", "manager": "Paul Marshall/Ian Wace",    "category": "Major Fund", "style": "Long-Short/Quant",      "aum_b": 62},
    {"name": "Jane Street Capital",      "cik": "0001580796", "manager": "Various",                   "category": "Major Fund", "style": "Quant/Market-Making",   "aum_b": 30},
    {"name": "Soros Fund Management",    "cik": "0001029155", "manager": "George Soros (family)",     "category": "Major Fund", "style": "Global Macro",         "aum_b": 7},
    {"name": "Farallon Capital",         "cik": "0000909661", "manager": "Andrew Spokes",             "category": "Major Fund", "style": "Event-Driven/Value",   "aum_b": 39},
    {"name": "King Street Capital",      "cik": "0001103487", "manager": "Brian Higgins",             "category": "Major Fund", "style": "Distressed/Credit",    "aum_b": 24},
    {"name": "Oaktree Capital",          "cik": "0000949924", "manager": "Howard Marks",              "category": "Major Fund", "style": "Distressed/Credit",    "aum_b": 19},

    # ── 🎯 Activist Investors ──
    {"name": "Starboard Value",          "cik": "0001383312", "manager": "Jeff Smith",                "category": "Activist",   "style": "Operational Activist", "aum_b": 8},
    {"name": "Trian Fund Management",    "cik": "0001345471", "manager": "Nelson Peltz",              "category": "Activist",   "style": "Operational Activist", "aum_b": 12},
    {"name": "ValueAct Capital",         "cik": "0001037976", "manager": "Mason Morfit",              "category": "Activist",   "style": "Constructivist",       "aum_b": 14},
    {"name": "JANA Partners",            "cik": "0001134124", "manager": "Barry Rosenstein",          "category": "Activist",   "style": "Event-Driven Activist","aum_b": 2},
    {"name": "Corvex Management",        "cik": "0001508155", "manager": "Keith Meister",             "category": "Activist",   "style": "Concentrated Activist","aum_b": 3},
    {"name": "Sachem Head Capital",      "cik": "0001567614", "manager": "Scott Ferguson",            "category": "Activist",   "style": "Constructivist",       "aum_b": 4},
    {"name": "Ancora Holdings",          "cik": "0001541618", "manager": "Frederick DiSanto",         "category": "Activist",   "style": "Small-Cap Activist",   "aum_b": 3},
    {"name": "Mantle Ridge",             "cik": "0001695228", "manager": "Paul Hilal",                "category": "Activist",   "style": "Concentrated Activist","aum_b": 3},
    {"name": "Engine Capital",           "cik": "0001608030", "manager": "Arnaud Ajdler",             "category": "Activist",   "style": "Small-Cap Activist",   "aum_b": 1},
    {"name": "Land & Buildings",         "cik": "0001542145", "manager": "Jonathan Litt",             "category": "Activist",   "style": "REIT Activist",        "aum_b": 0.5},

    # ── 📊 Sector Specialists ──
    {"name": "Baker Bros. Advisors",     "cik": "0001087615", "manager": "Julian/Felix Baker",        "category": "Specialist","style": "Biotech",               "aum_b": 15},
    {"name": "OrbiMed Advisors",         "cik": "0001055951", "manager": "Various",                   "category": "Specialist","style": "Healthcare",            "aum_b": 18},
    {"name": "RA Capital Management",    "cik": "0001539632", "manager": "Peter Kolchinsky",          "category": "Specialist","style": "Biotech",               "aum_b": 6},
    {"name": "Soroban Capital Partners", "cik": "0001541619", "manager": "Eric Mandelblatt",          "category": "Specialist","style": "Tech/Industrials",      "aum_b": 12},
    {"name": "Himalayan Capital",        "cik": "0001506991", "manager": "Li Lu",                     "category": "Specialist","style": "Asia/Value",             "aum_b": 3},
    {"name": "Ruane, Cunniff & Goldfarb","cik": "0000080333", "manager": "Sequoia Fund",              "category": "Specialist","style": "Concentrated Value",     "aum_b": 8},
    {"name": "GQG Partners",             "cik": "0001748825", "manager": "Rajiv Jain",                "category": "Specialist","style": "Global Quality",         "aum_b": 120},
    {"name": "Akre Capital Management",  "cik": "0001112747", "manager": "Chuck Akre",                "category": "Specialist","style": "Compounding Machines",   "aum_b": 14},
    {"name": "Markel Gayner Asset Mgmt", "cik": "0001096343", "manager": "Tom Gayner",                "category": "Specialist","style": "Quality/Insurance",     "aum_b": 10},
    {"name": "Dorsey Asset Management",  "cik": "0001608031", "manager": "John Dorsey",               "category": "Specialist","style": "Concentrated Growth",   "aum_b": 2},
]

# Categories for display/grouping
CATEGORIES = ["Legendary", "Tiger Cub", "Major Fund", "Activist", "Specialist"]


def get_fund(name: str = None, cik: str = None) -> dict | None:
    """Look up a fund by name or CIK."""
    for f in WATCHLIST:
        if name and f["name"].lower() == name.lower():
            return f
        if cik and f["cik"] == cik:
            return f
    return None


def get_funds_by_category(category: str) -> list[dict]:
    """Return all funds in a category."""
    return [f for f in WATCHLIST if f["category"] == category]


def get_all_ciks() -> list[str]:
    """Return all CIK numbers as strings."""
    return [f["cik"] for f in WATCHLIST]


def summary() -> str:
    """Human-readable watchlist summary."""
    lines = []
    for cat in CATEGORIES:
        funds = get_funds_by_category(cat)
        total_aum = sum(f["aum_b"] for f in funds)
        lines.append(f"  {cat}: {len(funds)} funds · ${total_aum:.0f}B AUM")
    lines.append(f"  TOTAL: {len(WATCHLIST)} funds")
    return "\n".join(lines)
