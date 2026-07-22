# Controlled Theme Set — Gate B

Status: Approved — Gate B Complete (Founder Review 22 Jul 2026)
Version: 1.0
Owner: Founder
Authority: Gate B artifact subordinate to the Constitution, Founder's Decisions, Approved Domain Specifications, and Approved Stable Design Plan v0.1; individual Theme definitions gain authority only through explicit Founder approval
Derived from: Constitution v0.3, Project Definition v0.1 (ALPHA-MOMENTUM-V0-SPEC §3), DESIGN-PLAN §6
Data Source: `docs/finviz.csv` — Finviz screener export (11,507 stocks, filtered to 143 operating-company industries)
Draft Authorization: per Founder Decision #17 (Gate B Authorization)
Supersedes: v0.1 (3 synthetic), v0.2 (11 broad sectors), v0.3 (40 sub-themes from dropdown CSV)

---

## 1. Purpose

This document defines the controlled set of Themes for the Alpha Momentum V0 design and fixture set. All 143 Themes are drawn from the **Industry** column of the Finviz stock screener export (`docs/finviz.csv`), as directed by Founder.

**Filter applied:** Exchange Traded Funds, Closed-End Funds, and Shell Companies excluded (not operating companies; incompatible with DS-309 universe of common stocks + ADRs).

Each Theme is assessed against the four selection criteria from ALPHA-MOMENTUM-V0-SPEC §3.1:

1. **Structural driver** — the theme represents a structural economic, technological, policy, or demographic driver
2. **Identifiable beneficiaries** — companies in the US-listed universe are mappable to Theme Relationship Roles
3. **Evidence availability** — sufficient public-domain evidence for realistic V0 fixtures
4. **Domain coverage** — testability, evidence diversity, lifecycle coverage, relationship-role coverage

All Themes in this document are **Proposed** until explicitly Approved by the Founder. This approval is **not** a buy recommendation or investment endorsement (DESIGN-PLAN §6).

**⚠️ NOT LIVE DATA — FOR V0 TESTING ONLY:** All tickers, company names, and industry classifications referenced in this document are public-domain identifiers from the Finviz screener. They do not represent live market data, current recommendations, or investment advice (SPEC §8.4).

---

## 2. Theme Inventory — 143 Industries by Sector

### 2.1 Technology (12 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 1 | TH-001 | Software - Application | 227 | Expansion | ADBE, ADP, ADSK, CRM, NOW, WDAY |
| 2 | TH-002 | Software - Infrastructure | 176 | Expansion | MSFT, ORCL, SNOW, DDOG, MDB, NET |
| 3 | TH-003 | Information Technology Services | 75 | Emerging Leadership | ACN, IBM, FIS, FISV, GPN, JKHY |
| 4 | TH-004 | Semiconductors | 71 | Expansion | NVDA, AMD, AVGO, QCOM, INTC, TXN |
| 5 | TH-005 | Electronic Components | 46 | Emerging Leadership | APH, GLW, TEL, FLEX, JBL, CLS |
| 6 | TH-006 | Communication Equipment | 44 | Emerging Leadership | CSCO, ANET, MSI, HPE, JNPR, CIEN |
| 7 | TH-007 | Computer Hardware | 41 | Crowded / Late | AAPL, DELL, HPQ, NTAP, PSTG, SMCI |
| 8 | TH-008 | Scientific & Technical Instruments | 34 | Emerging Leadership | KEYS, TDY, TRMB, CGNX, NOVT, MKSI |
| 9 | TH-009 | Semiconductor Equipment & Materials | 29 | Expansion | AMAT, LRCX, KLAC, ASML, TSM, AMKR |
| 10 | TH-010 | Solar | 22 | Formation | ENPH, FSLR, SEDG, RUN, CSIQ, ARRY |
| 11 | TH-011 | Consumer Electronics | 19 | Crowded / Late | AAPL, SONY, GRMN, SONO, GPRO, VUZI |
| 12 | TH-012 | Electronics & Computer Distribution | 8 | Crowded / Late | ARW, AVT, SNX, NSIT, CNXN, SCSC |

### 2.2 Healthcare (11 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 13 | TH-013 | Biotechnology | 594 | Formation | AMGN, GILD, REGN, BIIB, MRNA, ALNY |
| 14 | TH-014 | Medical Devices | 139 | Emerging Leadership | ABT, MDT, BSX, SYK, ISRG, EW |
| 15 | TH-015 | Drug Manufacturers - Specialty & Generic | 86 | Emerging Leadership | TEVA, VTRS, CTLT, PRGO, JAZZ, ELAN |
| 16 | TH-016 | Medical Instruments & Supplies | 56 | Emerging Leadership | TMO, DHR, BDX, BAX, HOLX, WAT |
| 17 | TH-017 | Medical Care Facilities | 49 | Emerging Leadership | HCA, THC, UHS, CHE, EHC, SEM |
| 18 | TH-018 | Diagnostics & Research | 46 | Emerging Leadership | A, DGX, LH, IQV, CRL, NEOG |
| 19 | TH-019 | Health Information Services | 45 | Formation | VEEV, CERT, MDRX, TDOC, AMWL, PRVA |
| 20 | TH-020 | Drug Manufacturers - General | 21 | Expansion | LLY, JNJ, MRK, ABBV, PFE, BMY |
| 21 | TH-021 | Medical Distribution | 11 | Crowded / Late | MCK, ABC, CAH, HSIC, OMI, PDCO |
| 22 | TH-022 | Healthcare Plans | 11 | Crowded / Late | UNH, ELV, CI, CNC, HUM, MOH |
| 23 | TH-023 | Pharmaceutical Retailers | 6 | Crowded / Late | WBA, RAD, PETS, HITI, SCNX, WGRX |

### 2.3 Financial (14 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 24 | TH-024 | Banks - Regional | 323 | Emerging Leadership | PNC, USB, TFC, FITB, CFG, KEY |
| 25 | TH-025 | Asset Management | 147 | Emerging Leadership | BLK, BK, STT, TROW, AMP, BEN |
| 26 | TH-026 | Capital Markets | 94 | Emerging Leadership | GS, MS, SCHW, IBKR, RJF, SF |
| 27 | TH-027 | Credit Services | 52 | Emerging Leadership | V, MA, AXP, DFS, COF, SYF |
| 28 | TH-028 | Insurance - Property & Casualty | 44 | Crowded / Late | TRV, ALL, PGR, CB, CINF, WRB |
| 29 | TH-029 | Insurance Brokers | 22 | Crowded / Late | MMC, AON, AJG, BRO, WTW, RYAN |
| 30 | TH-030 | Banks - Diversified | 20 | Crowded / Late | JPM, BAC, C, WFC, BMO, BNS |
| 31 | TH-031 | Insurance - Life | 18 | Crowded / Late | MET, PRU, AFL, LNC, UNM, GL |
| 32 | TH-032 | Insurance - Specialty | 17 | Emerging Leadership | FNF, FAF, ESNT, AGI, ACT, AMSF |
| 33 | TH-033 | Financial Data & Stock Exchanges | 15 | Emerging Leadership | SPGI, MSCI, CME, ICE, COIN, NDAQ |
| 34 | TH-034 | Mortgage Finance | 13 | Formation | RKT, UWMC, COOP, PFSI, GHLD, LDI |
| 35 | TH-035 | Insurance - Diversified | 12 | Crowded / Late | BRK-B, AIG, ACGL, HIG, AEG, BNT |
| 36 | TH-036 | Insurance - Reinsurance | 8 | Crowded / Late | RGA, RNR, EG, GLRE, SPNT, OXBR |
| 37 | TH-037 | Financial Conglomerates | 7 | Crowded / Late | FRHC, HTH, IX, RILY, TMS, TREE, VOYA |

### 2.4 Communication Services (7 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 38 | TH-038 | Internet Content & Information | 71 | Emerging Leadership | GOOGL, META, BIDU, SNAP, PINS, TWLO |
| 39 | TH-039 | Telecom Services | 57 | Crowded / Late | T, VZ, TMUS, CHTR, CMCSA, LUMN |
| 40 | TH-040 | Entertainment | 49 | Crowded / Late | DIS, NFLX, WBD, SPOT, LYV, ROKU |
| 41 | TH-041 | Advertising Agencies | 39 | Emerging Leadership | OMC, IPG, PUBGY, CCO, WPP, STGW |
| 42 | TH-042 | Electronic Gaming & Multimedia | 22 | Emerging Leadership | EA, TTWO, RBLX, U, NTES, PLTK |
| 43 | TH-043 | Broadcasting | 15 | Deterioration | GTN, IHRT, FUBO, CAST, CURI, BBGI |
| 44 | TH-044 | Publishing | 8 | Deterioration | NYT, WLY, PSO, SCHL, LEE, EDUC |

### 2.5 Consumer Cyclical (23 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 45 | TH-045 | Auto Parts | 55 | Emerging Leadership | APTV, ALV, BWA, LEA, GNTX, ADNT |
| 46 | TH-046 | Restaurants | 52 | Emerging Leadership | MCD, SBUX, YUM, QSR, DPZ, CMG |
| 47 | TH-047 | Specialty Retail | 46 | Emerging Leadership | ORLY, AZO, TSCO, BBWI, FIVE, DKS |
| 48 | TH-048 | Internet Retail | 39 | Expansion | AMZN, BABA, PDD, MELI, CART, CHWY |
| 49 | TH-049 | Leisure | 33 | Emerging Leadership | CCL, RCL, NCLH, HAS, MAT, SEAS |
| 50 | TH-050 | Apparel Retail | 32 | Crowded / Late | TJX, ROST, BURL, ANF, GPS, AEO |
| 51 | TH-051 | Auto Manufacturers | 30 | Emerging Leadership | TSLA, F, GM, HMC, TM, RIVN |
| 52 | TH-052 | Furnishings, Fixtures & Appliances | 30 | Crowded / Late | WHR, TPX, MHK, LEG, SNBR, COOK |
| 53 | TH-053 | Auto & Truck Dealerships | 25 | Crowded / Late | KMX, AN, PAG, GPI, LAD, ABG |
| 54 | TH-054 | Apparel Manufacturing | 23 | Crowded / Late | NKE, VFC, RL, PVH, UAA, GIL |
| 55 | TH-055 | Packaging & Containers | 22 | Crowded / Late | BALL, AMCR, AVY, GPK, SEE, CCK |
| 56 | TH-056 | Residential Construction | 19 | Formation | DHI, LEN, NVR, PHM, TOL, KBH |
| 57 | TH-057 | Travel Services | 18 | Emerging Leadership | BKNG, ABNB, EXPE, TCOM, CCL, MMYT |
| 58 | TH-058 | Resorts & Casinos | 17 | Crowded / Late | LVS, WYNN, MGM, CZR, BYD, HGV |
| 59 | TH-059 | Recreational Vehicles | 15 | Crowded / Late | HOG, THO, WGO, LCII, BC, MAMO |
| 60 | TH-060 | Gambling | 14 | Emerging Leadership | DKNG, FLUT, CHDN, GENI, SRAD, GAMB |
| 61 | TH-061 | Footwear & Accessories | 14 | Crowded / Late | NKE, DECK, CROX, SKX, BIRK, WWW |
| 62 | TH-062 | Personal Services | 13 | Crowded / Late | HRB, BFAM, MED, WW, CSV, FTDR |
| 63 | TH-063 | Lodging | 11 | Emerging Leadership | MAR, HLT, IHG, H, WH, CHH |
| 64 | TH-064 | Luxury Goods | 11 | Emerging Leadership | LVMUY, TPR, CPRI, MOV, REAL, BRLT |
| 65 | TH-065 | Textile Manufacturing | 5 | Deterioration | AIN, CULP, UFI, PASW, SMJF |
| 66 | TH-066 | Home Improvement Retail | 5 | Crowded / Late | HD, LOW, FND, LL, LIVE |
| 67 | TH-067 | Department Stores | 4 | Deterioration | KSS, M, DDS, JWN |

### 2.6 Consumer Defensive (12 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 68 | TH-068 | Packaged Foods | 61 | Crowded / Late | K, GIS, HSY, MKC, CAG, SJM |
| 69 | TH-069 | Education & Training Services | 42 | Formation | CHGG, COUR, UDMY, LOPE, AFYA, APEI |
| 70 | TH-070 | Household & Personal Products | 30 | Crowded / Late | PG, CL, EL, CLX, COTY, NWL |
| 71 | TH-071 | Farm Products | 20 | Emerging Leadership | ADM, BG, CALM, TSN, AGRO, LMNR |
| 72 | TH-072 | Beverages - Non-Alcoholic | 18 | Crowded / Late | KO, PEP, MNST, CELH, FIZZ, COCO |
| 73 | TH-073 | Grocery Stores | 13 | Crowded / Late | KR, ACI, IMKTA, NGVC, SFM, GO |
| 74 | TH-074 | Beverages - Wineries & Distilleries | 12 | Crowded / Late | STZ, BF-B, DEO, MGPI, BF-A, SAM |
| 75 | TH-075 | Food Distribution | 12 | Crowded / Late | SYY, USFD, PFGC, CHEF, ANDE, AVO |
| 76 | TH-076 | Tobacco | 11 | Deterioration | MO, PM, BTI, GNLN, ISPR, RLX |
| 77 | TH-077 | Discount Stores | 9 | Crowded / Late | WMT, COST, TGT, DG, DLTR, BJ |
| 78 | TH-078 | Beverages - Brewers | 7 | Crowded / Late | BUD, TAP, SAM, STZ, CCU, ABEV |
| 79 | TH-079 | Confectioners | 5 | Crowded / Late | MDLZ, HSY, TR, RMCF, SOWG |

### 2.7 Industrials (24 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 80 | TH-080 | Aerospace & Defense | 90 | Emerging Leadership | LMT, RTX, BA, GD, NOC, LHX |
| 81 | TH-081 | Specialty Industrial Machinery | 82 | Emerging Leadership | CAT, DE, ITW, PH, CMI, ROP |
|| 82 | TH-082 | Engineering & Construction | 53 | Formation | ACM, J, PWR, FLR, BLDR, FIX, BEEP |
| 83 | TH-083 | Electrical Equipment & Parts | 51 | Emerging Leadership | ETN, EMR, AME, HUBB, ATKR, AYI |
| 84 | TH-084 | Specialty Business Services | 44 | Emerging Leadership | GPN, FLT, ADT, BR, ARM, BAH |
| 85 | TH-085 | Marine Shipping | 38 | Emerging Leadership | MATX, CMRE, SBLK, GNK, DAC, DSX |
| 86 | TH-086 | Building Products & Equipment | 36 | Formation | CARR, JCI, MAS, OC, BLDR, FBIN |
| 87 | TH-087 | Integrated Freight & Logistics | 32 | Emerging Leadership | UPS, FDX, CHRW, EXPD, GXO, HUBG |
| 88 | TH-088 | Conglomerates | 28 | Crowded / Late | HON, MMM, GE, ITT, BOC, CODI |
| 89 | TH-089 | Farm & Heavy Construction Machinery | 26 | Emerging Leadership | CAT, DE, AGCO, CNHI, OSK, TEX |
| 90 | TH-090 | Security & Protection Services | 23 | Emerging Leadership | ALLE, BCO, ADT, BRC, MSA, CIX |
| 91 | TH-091 | Consulting Services | 22 | Emerging Leadership | EFX, BAH, FCN, CRAI, EXPO, ICFI |
| 92 | TH-092 | Industrial Distribution | 22 | Emerging Leadership | FAST, GWW, AIT, WSO, BXC, MSM |
| 93 | TH-093 | Rental & Leasing Services | 21 | Formation | URI, AER, AL, CAR, GATX, CTOS |
| 94 | TH-094 | Waste Management | 19 | Emerging Leadership | WM, RSG, WCN, CLH, CWST, MEG |
| 95 | TH-095 | Airlines | 18 | Crowded / Late | DAL, UAL, LUV, AAL, ALK, JBLU |
| 96 | TH-096 | Metal Fabrication | 18 | Formation | CRS, ATI, CMC, WOR, IIIN, ESAB |
| 97 | TH-097 | Staffing & Employment Services | 17 | Crowded / Late | NSP, KFY, RHI, MAN, KELYA, BBSI |
| 98 | TH-098 | Pollution & Treatment Controls | 16 | Formation | ECL, FTEK, CECO, ERII, CLIR, ARQ |
| 99 | TH-099 | Trucking | 16 | Emerging Leadership | ODFL, KNX, SAIA, XPO, ARCB, WERN |
| 100 | TH-100 | Railroads | 12 | Crowded / Late | UNP, CSX, NSC, CP, CNI, WAB |
| 101 | TH-101 | Tools & Accessories | 10 | Emerging Leadership | SNA, SWK, TTC, LECO, KMT, HLMN |
| 102 | TH-102 | Airports & Air Services | 8 | Emerging Leadership | PAC, ASR, OMAB, CAAP, JOBY, ACHR |
|| 103 | TH-103 | Business Equipment & Supplies | 5 | Deterioration | XRX, ACCO, EBF, ACTG, EHGO |

### 2.8 Energy (8 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 105 | TH-105 | Oil & Gas E&P | 78 | Deterioration | XOM, CVX, COP, EOG, PXD, DVN |
| 106 | TH-106 | Oil & Gas Midstream | 58 | Deterioration | KMI, WMB, EPD, ET, MPLX, OKB |
| 107 | TH-107 | Oil & Gas Equipment & Services | 51 | Deterioration | SLB, HAL, BKR, WFRD, NOV, FTI |
| 108 | TH-108 | Oil & Gas Integrated | 20 | Deterioration | XOM, CVX, BP, SHEL, TTE, EQNR |
| 109 | TH-109 | Oil & Gas Refining & Marketing | 19 | Deterioration | MPC, VLO, PSX, DINO, PBF, DK |
| 110 | TH-110 | Uranium | 13 | Formation | CCJ, UEC, UUUU, DNN, LEU, EU |
| 111 | TH-111 | Oil & Gas Drilling | 10 | Deterioration | RIG, NBR, HP, PTEN, SDRL, BORR |
| 112 | TH-112 | Thermal Coal | 5 | Deterioration | BTU, ARLP, NC, NRP, CNR |

### 2.9 Basic Materials (14 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 113 | TH-113 | Specialty Chemicals | 59 | Emerging Leadership | LIN, SHW, ECL, APD, PPG, DD |
| 114 | TH-114 | Other Industrial Metals & Mining | 54 | Formation | BHP, RIO, VALE, MP, TECK, CMP |
| 115 | TH-115 | Gold | 51 | Emerging Leadership | NEM, GOLD, AEM, KGC, GFI, AU |
| 116 | TH-116 | Other Precious Metals & Mining | 20 | Formation | WPM, FSM, AG, HL, BVN, EXK |
| 117 | TH-117 | Steel | 20 | Formation | NUE, STLD, CLF, X, GGB, RS |
| 118 | TH-118 | Chemicals | 17 | Emerging Leadership | DOW, CE, LYB, WLK, EMN, OLN |
| 119 | TH-119 | Building Materials | 17 | Formation | CRH, EXP, VMC, MLM, CX, JHX |
| 120 | TH-120 | Agricultural Inputs | 13 | Emerging Leadership | MOS, CF, NTR, CTVA, FMC, ICL |
| 121 | TH-121 | Copper | 7 | Formation | FCX, SCCO, HBM, ERO, TGB, IE |
| 122 | TH-122 | Silver | 6 | Formation | AG, EXK, SVM, HSLV, NEWP, AYA |
| 123 | TH-123 | Lumber & Wood Production | 6 | Formation | WFG, UFPI, BCC, SSD, NWGL, JCTC |
| 124 | TH-124 | Coking Coal | 5 | Formation | AMR, HCC, METC, SXC, AREC |
| 125 | TH-125 | Paper & Paper Products | 5 | Crowded / Late | IP, SLVM, MERC, CLW, ITP |
| 126 | TH-126 | Aluminum | 4 | Formation | AA, CENX, KALU, CSTM |

### 2.10 Real Estate (12 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 127 | TH-127 | Real Estate Services | 45 | Formation | CBRE, JLL, CWK, BEKE, COMP, RDFN |
| 128 | TH-128 | REIT - Mortgage | 39 | Formation | AGNC, NLY, STWD, ARI, ABR, RITM |
| 129 | TH-129 | REIT - Retail | 27 | Formation | SPG, O, KIM, REG, BXP-WI, ADC |
| 130 | TH-130 | REIT - Residential | 21 | Formation | AVB, EQR, CPT, MAA, UDR, AMH |
| 131 | TH-131 | REIT - Office | 20 | Deterioration | BXP, ARE, VNO, CUZ, KRC, DEI |
| 132 | TH-132 | REIT - Specialty | 19 | Emerging Leadership | AMT, EQIX, DLR, CCI, PLD, PSA |
| 133 | TH-133 | REIT - Diversified | 17 | Crowded / Late | O, WPC, VICI, GLPI, EPRT, FVR |
| 134 | TH-134 | REIT - Healthcare Facilities | 17 | Formation | WELL, VTR, PEAK, DOC, NHI, CTRE |
| 135 | TH-135 | REIT - Industrial | 17 | Emerging Leadership | PLD, FR, EXR, COLD, EGP, STAG |
| 136 | TH-136 | REIT - Hotel & Motel | 15 | Formation | HST, APLE, PK, DRH, INN, CLDT |
| 137 | TH-137 | Real Estate - Development | 14 | Formation | FOR, CCS, LRE, FPH, JFB, AXR |
| 138 | TH-138 | Real Estate - Diversified | 3 | Crowded / Late | HHH, JOE, STRS |

### 2.11 Utilities (6 Industries)

| # | Theme ID | Industry | Stocks | Lifecycle | Key Tickers |
|---|---|---|---|---|---|
| 139 | TH-139 | Utilities - Regulated Electric | 41 | Emerging Leadership | NEE, DUK, SO, AEP, EXC, XEL |
| 140 | TH-140 | Utilities - Renewable | 24 | Formation | NEE, CWEN, BEPC, AY, PEG, HASI |
| 141 | TH-141 | Utilities - Regulated Gas | 16 | Emerging Leadership | ATO, NI, BKH, OGS, NJR, SR |
| 142 | TH-142 | Utilities - Regulated Water | 13 | Emerging Leadership | AWK, WTRG, AWR, CWT, ARTNA, MSEX |
| 143 | TH-143 | Utilities - Independent Power Producers | 9 | Formation | CEG, VST, NRG, TAC, KEN, HNRG |
| 144 | TH-144 | Utilities - Diversified | 7 | Emerging Leadership | D, SRE, AEE, CMS, LNT, ES |

---

## 3. Summary Statistics

| Metric | Value |
|---|---|
| **Total Themes** | **143** |
| **Sectors represented** | 11 of 11 |
| **Total underlying stocks** | ~5,500 operating companies |
| **Largest theme** | Biotechnology (594 stocks) |
| **Smallest theme** | Real Estate - Diversified (3 stocks) |
| **Lifecycle: Expansion** | 6 themes (TH-001, TH-002, TH-004, TH-009, TH-020, TH-048) |
| **Lifecycle: Emerging Leadership** | ~55 themes |
| **Lifecycle: Crowded / Late** | ~35 themes |
| **Lifecycle: Formation** | ~33 themes |
| **Lifecycle: Deterioration** | ~14 themes |

---

## 4. Lifecycle Assignment

Lifecycle stages are assigned at the industry level based on general market conditions as of July 2026. Each stage reflects the industry's position in its development cycle:

| Stage | Description | Themes | V0 Relevance |
|---|---|---|---|
| **Expansion** 🟢 | Broad adoption, multiple independent growth vectors | Semis, Cloud, Software, Semi Equipment, Drug Manufacturers General, E-commerce, AI-related | Primary hunting ground — confirmed uptrend, Stage 2 advancing |
| **Emerging Leadership** 🟡 | Leaders and challengers distinguishable; operational evidence exists | ~55 industries including Most Healthcare, FinTech, Defense, Restaurants, Travel, Aerospace, Waste Mgmt | Secondary hunting ground — watch for uptrend transitions |
| **Formation** 🔵 | Early indicators; structural evidence but no consensus | ~35 industries including Solar, Biotech, Health IT, Residential Construction, Clean Energy, Space, Quantum-adjacent | High potential, high uncertainty — monitor, don't chase |
| **Crowded / Late** 🟠 | Widely recognized; limited upside surprise; crowding risk material | ~35 industries including Tobacco, Broadcasting, Paper, Telecom, Department Stores, Consumer Staples | Caution zone — limited alpha potential |
| **Deterioration** 🔴 | Structural decline; leadership rotating or exiting | Energy (all 7 sub-industries), REIT Office, Education, Publishing, Broadcasting, Tobacco, Textile, Business Equipment | Avoid long; short candidates (Founder discretion) |

> **Founder note:** Lifecycle assignments are proposed defaults based on general market conditions. The Founder may reassign any industry to a different lifecycle stage based on their market view. Deterioration themes are identified for avoidance and potential short opportunity identification. Momentum strategy draws on the Founder's Stage 2 uptrend approach — exact rule packs (O'Neil, Minervini) remain deferred per DESIGN-PLAN.md §11.

---

## 5. Domain Coverage

### 5.1 Selection Criteria (SPEC §3.1)

| Criterion | Assessment |
|---|---|
| 1. **Structural driver** | ✅ All 143 industries represent structural economic classifications — not short-term catalysts |
| 2. **Identifiable beneficiaries** | ✅ ~5,500 US-listed operating companies mapped to industries via Finviz classification |
| 3. **Evidence availability** | ✅ Industry-level data publicly available; company filings (10-K/10-Q) provide granular evidence |
| 4. **Domain coverage** | ✅ Full lifecycle spectrum (Formation → Deterioration); all 11 sectors; every relationship role distributable across the set |

### 5.2 Relationship Role Coverage

All 8 Theme Relationship Roles can be mapped across the 143 themes:

| Role | Example Mappings |
|---|---|
| **Confirmed Leader** | NVDA (Semis), LLY (Drug Mfg), JPM (Banks-Diversified), UNH (Healthcare Plans) |
| **Emerging Challenger** | AMD (Semis), RIVN (Auto Mfg), SOFI (Credit Services), CEG (Utilities-IPP) |
| **Direct Beneficiary** | Present in virtually every Candidate–Theme relationship |
| **Enabler** | AVGO (Semis→AI enabler), APH (Electronic Components→enabler to multiple industries), ICE (Financial Data→market infrastructure) |
| **Bottleneck Owner** | ASML (Semi Equipment→lithography monopoly), AMT (REIT-Specialty→tower infrastructure), FCX (Copper→electrification bottleneck) |
| **Second-order Beneficiary** | ARW (Electronics Distribution→downstream from semis), FWRD (Freight→downstream from manufacturing), ETSY (Internet Retail→downstream from e-commerce infra) |
| **Watchlist Member** | Numerous across Formation-stage industries |
| **Former Leader** | INTC (Semis), GE (Conglomerates→pre-split), WBA (Pharm Retail) |
| **Deteriorating Member** | XOM/CVX (Energy), KSS/M (Department Stores), MO (Tobacco) |

### 5.3 Minimum Fixture Requirements (SPEC §8.3)

| Requirement | Status | How Met |
|---|---|---|
| ≥2-3 Founder-approved themes | ✅ | 143 themes proposed |
| ≥1 theme with supporting + contradicting evidence | ✅ | Every sector has both (see §6) |
| ≥1 theme with explicit missing-evidence markers | ✅ | Every sector has missing evidence (see §6) |
| ≥1 Candidate with multiple relationship roles | ✅ | e.g., NVDA: Semis + Semi Equipment + AI-adjacent; AAPL: Consumer Electronics + Computer Hardware |
| Leadership State transition example | ✅ | INTC: Former Leader (Semis); GE: pre/post-split transformation |
| Lifecycle transition example | ✅ | Energy: Expansion→Deterioration transition evident across multiple sub-industries |
| ≥1 Human Override in Pending state | ✅ | Gate C fixture design |
| ≥1 Research Queue returning zero | ✅ | Gate C fixture design |

---

## 6. V0 Screening Methodology — Stock-First + Theme Enrichment

> **Scope note:** This section is an informative reference summarizing the Stock-First + Theme Enrichment approach (Approach C) approved under Gate B Founder Review Q2. The canonical pipeline design and all stage-by-stage contracts are in `PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md` (Gate A artifact, DS-501 through DS-513). This section does not override or duplicate Gate A pipeline authority.

**Founder Decision:** Q2 — Industry size normalization resolved via Approach C.

### 6.1 Principle

The question is not "how many stocks in this industry?" but "is this stock buyable?"

Themes provide context; stock quality drives candidate selection. No arbitrary quotas, floors, ceilings, or normalization formulas.

### 6.2 Two-Pass Pipeline

```
Pass 1: Stock-Level Screening (Theme-Agnostic)
  ┌─────────────────────────────────────────┐
  │ Universe: ~5,500 operating companies    │
  │   → Absolute quality thresholds:         │
  │     • RS Rating (deferred)               │
  │     • EPS growth trajectory (deferred)   │
  │     • Volume / liquidity minimum (deferred)│
  │     • Price structure — Stage 2 (deferred) │
  │   → Result: N qualified candidates (notional — no target range) |
  └─────────────────────────────────────────┘
                    ↓
Pass 2: Theme Enrichment (Map to Context)
  ┌─────────────────────────────────────────┐
  │ Qualified stocks → map to Theme via     │
  │   Finviz Industry classification        │
  │   → Each stock inherits Theme context:  │
  │     • Lifecycle stage                   │
  │     • Theme Quality                     │
  │     • Supporting/contradicting evidence │
  │   → Result: Theme-tagged candidates     │
  └─────────────────────────────────────────┘
                    ↓
Research Queue: Theme-First
  ┌─────────────────────────────────────────┐
  │ Group by Theme → within Theme, order    │
  │   by strategy-owned prioritization      │
  │   • Themes with many candidates =       │
  │     genuine momentum breadth            │
  │   • Themes with zero candidates =       │
  │     Honest Empty (no setup yet)          │
  │   • Queue capacity is adaptive —        │
  │     returns only what qualifies         │
  └─────────────────────────────────────────┘
```

### 6.3 Why This Works for All Industry Sizes

| Scenario | Behavior | Example |
|---|---|---|
| **Large industry** (594 stocks) | Many stocks screened, only quality passes. Biotech may have 30 candidates or 3 — depends on market conditions, not industry size | Biotech → only stocks in Stage 2 uptrend with strong RS pass |
| **Medium industry** (50-100 stocks) | Typical distribution. 5-15 candidates when sector is in favor | Aerospace & Defense → leaders emerge naturally |
| **Small industry** (3-5 stocks) | Small absolute number of stocks. May return 0-3 candidates. No padding — if none qualify, queue stays empty for that theme | Real Estate - Diversified (3 stocks) → may return 0 candidates |
| **Single-stock industry** (merged) | All single-stock edge cases resolved by merging into parent industry; no 1-stock themes remain | TH-104 Infrastructure → merged into TH-082 Engineering & Construction |

### 6.4 Key Properties

- ✅ **No arbitrary normalization** — no sqrt, ceiling, floor, or quota formulas invented
- ✅ **Adaptive Capacity** — queue size determined by quality, not targets (Founder Decision #9)
- ✅ **Honest Empty States** — themes without qualified candidates are empty, not padded (DNA-016)
- ✅ **Theme-first queue preserved** — candidates still grouped by Theme (Constitution §14)
- ✅ **Four quality dimensions separate** — Candidate Quality, Theme Quality, Entry Readiness, Data Confidence remain distinct (Constitution §10)
- ✅ **Stock-first future-proof** — pipeline preserves stock-first discovery path (SPEC §4.4)
- ✅ **Exact thresholds deferred** — RS, EPS, volume, price-structure rules remain deferred to approved rule packs

---

## 7. Evidence Structure by Sector

### 7.1 Technology

| Category | Evidence |
|---|---|
| **Supporting** | AI compute demand (NVDA data center revenue 200%+ YoY); Cloud migration 20%+ growth (AWS/Azure/GCP); Enterprise SaaS model recurring revenue visibility; Semiconductor equipment orders supporting multi-year expansion; CHIPS Act manufacturing incentives |
| **Contradicting** | AI efficiency (DeepSeek) → less compute per task = slower hardware demand; Open-source AI models commoditizing proprietary software; Cloud cost optimization slowing hyperscaler growth from peak; Semiconductor cycle historically boom-bust |
| **Missing** | Enterprise AI ROI data (most deployments < 2 years old); Inference-to-training compute ratio long-term; AI PC adoption rate — early, unclear consumer demand; Solar project economics at sustained higher interest rates |

### 7.2 Healthcare

| Category | Evidence |
|---|---|
| **Supporting** | GLP-1 market $100B+ projected by 2030; 65+ population growing 10,000/day in US; Biotech innovation: ADCs, CRISPR therapies reaching market; Medicare Part D GLP-1 coverage (2024 guidance); Medical device procedure volume normalization post-COVID |
| **Contradicting** | GLP-1 long-term adherence < 50% at 12 months (real-world data); Drug pricing pressure: IRA negotiations, PBM reform; Patent cliffs: Keytruda 2028+, Humira biosimilars already launched; Pharmacy retail foot traffic declining |
| **Missing** | 10+ year GLP-1 safety data; Pediatric long-term metabolic effects; Real-world cost-effectiveness vs. bariatric surgery at population scale; AI diagnostics clinical validation timeline |

### 7.3 Financial

| Category | Evidence |
|---|---|
| **Supporting** | Net interest margins stabilizing as rate environment normalizes; Investment banking fees recovering (M&A, IPO pipeline); Wealth management AUM at record highs; Credit card spending resilient; Insurance hardening cycle in P&C |
| **Contradicting** | CRE exposure: office and retail property values declining; $1.5T CRE debt maturing 2025-2027 → refinancing risk; Private credit disintermediating bank lending; Regional bank consolidation uncertainty; Credit card delinquencies rising among lower-income |
| **Missing** | Credit loss severity if unemployment rises above 5%; Duration of private credit growth cycle — data opaque; CRE distress magnitude — how much forced selling; Basel III Endgame capital requirement impact |

### 7.4 Communication Services

| Category | Evidence |
|---|---|
| **Supporting** | Digital ad spending growing 10-15% annually; Streaming subscriber growth continues; AI-powered ad targeting improving ROAS; 5G fixed wireless gaining broadband market share |
| **Contradicting** | TikTok regulatory risk; Streaming password-sharing benefits fading; 5G ROI unclear (heavy capex, limited ARPU uplift); Broadcasting: cord-cutting structural; Publishing: print decline continuing; AI-generated content flooding platforms |
| **Missing** | Streaming industry consolidation timeline; Impact of generative AI search on Google ad model; Telecom fiber overbuild risk; Traditional media AI disruption timeline |

### 7.5 Consumer (Cyclical + Defensive)

| Category | Evidence |
|---|---|
| **Supporting** | US consumer spending resilient: real PCE growing ~2.5% YoY; E-commerce penetration still gaining (~1pp/year); Brand pricing power intact (CPG companies); Travel/experiences spending elevated post-COVID; Discount retail gaining share |
| **Contradicting** | Credit card delinquencies at decade highs (NY Fed); Student loan payments resumed ($1.6T outstanding); Retail bankruptcies increasing; Auto loan delinquencies rising; Private label share gains (store brands 20%+); GLP-1 impact on food/alcohol consumption |
| **Missing** | Consumer resilience if unemployment rises to 5%+; EV adoption rate (mass-market transition); GLP-1 long-term impact on food industry structure; Tariff impact on imported consumer goods pricing |

### 7.6 Industrials

| Category | Evidence |
|---|---|
| **Supporting** | IIJA: $1.2T infrastructure bill — projects in early construction; Manufacturing construction at record highs (CHIPS + IRA + reshoring); Defense spending at post-Cold War highs ($2.4T globally); Aerospace backlog ~15,000 aircraft; Railroad pricing power intact |
| **Contradicting** | Mega-project cost overruns and delays historically common; Boeing quality/safety issues limiting deliveries; Political risk: IRA/IIJA modification under administration change; Labor shortages in skilled trades limiting execution; Trucking cycle near bottom |
| **Missing** | Actual vs. announced manufacturing job creation; Infrastructure spending multiplier effects; Automation ROI at current technology maturity; Defense spending sustainability at current fiscal deficit |

### 7.7 Energy

| Category | Evidence |
|---|---|
| **Supporting** (near-term) | Oil prices supported by OPEC+ supply management + geopolitical risk premium; LNG export capacity doubling from US Gulf Coast (2024-2028); Energy FCF yields among highest in S&P 500; Record buybacks + dividends; Uranium: nuclear renaissance (tech PPAs, SMR development) |
| **Contradicting** | IEA: global oil demand peaking by 2030 under stated policies; Renewable energy now cheaper than fossil fuels (LCOE); EV penetration reducing transportation fuel demand structurally; ESG-driven capital exodus from fossil fuels; Coal: structural decline accelerating |
| **Missing** | Peak oil demand timing — IEA vs. OPEC diverge by 15+ years; Carbon capture and hydrogen viability at scale; Geopolitical supply disruption probability; Nuclear SMR commercial viability timeline |

### 7.8 Basic Materials

| Category | Evidence |
|---|---|
| **Supporting** | Copper: structural deficit projected 2027+ (electrification, grid, EVs); Gold: central bank buying at record levels (1,000+ tonnes/year); Electrification mineral demand structurally higher; US housing shortage supports construction materials |
| **Contradicting** | China property crisis: 30%+ decline in new housing starts since 2021 peak — major commodity demand destruction; Mining cost inflation eroding margins; Recycling/substitution reducing primary commodity demand; Chemical industry overcapacity from China exports |
| **Missing** | Copper substitution rate in electrification applications; New mine development timeline: 7–15 years discovery to production; Lithium supply response — new projects may overshoot; Climate change impact on agricultural yields |

### 7.9 Real Estate

| Category | Evidence |
|---|---|
| **Supporting** | Data center REITs: leasing at records — AI/hyperscaler demand driving 20%+ rent growth; Tower REITs: 5G densification driving lease-up; Industrial/logistics: vacancy still low (~5%); Rate cut cycle supports REIT valuations |
| **Contradicting** | Office: 19%+ vacancy, values down 30%+ from peak — remote work structural; $1.5T CRE debt maturing by 2027 → refinancing at higher rates; Retail REITs: brick-and-mortar foot traffic declining; Regional bank CRE exposure |
| **Missing** | Office demand stabilization timeline; CRE distress magnitude — how much forced selling; Data center power availability — interconnection queue delays; Mortgage REIT: prepayment and spread duration risk |

### 7.10 Utilities

| Category | Evidence |
|---|---|
| **Supporting** | PJM interconnection queue: 40+ GW of data center load; Utility IRPs forecasting significant load growth for first time in 20 years; IRA clean energy tax credits providing multi-year policy visibility; Nuclear renaissance: tech companies signing PPAs; Regulated model = predictable returns |
| **Contradicting** | Rate case risk: PUCs may not approve full capex recovery; AI efficiency could reduce data center power intensity; Distributed generation reducing utility throughput; Nuclear: NRC licensing 5-10 years for new reactors |
| **Missing** | Actual vs. forecast data center load growth — forecasts could overshoot; Rate case outcomes — most major cases pending; SMR (Small Modular Reactor) commercial viability; Grid-scale storage economics at scale |

---

## 8. Founder Review — Resolved

| # | Question | Resolution | Date |
|---|---|---|---|
| Q1 | **Lifecycle assignment:** 144 industries ตรงกับ Jarvis มั้ย? | ✅ **ตรง** — ไม่ต้องปรับ lifecycle ใดๆ | 22 Jul 2026 |
| Q2 | **Industry size normalization:** industry ใหญ่ vs เล็ก จะ normalize ยังไง? | ✅ **Approach C** — Stock-First + Theme Enrichment (two-pass pipeline). หุ้นเลือก theme ไม่ใช่ theme เลือกหุ้น ไม่มี arbitrary quota/formula | 22 Jul 2026 |
| Q3 | **TH-104 Infrastructure Operations (BEEP):** เก็บไว้หรือรวม? | ✅ **รวม** เข้า TH-082 Engineering & Construction (53 stocks). BEEP = mobile infrastructure → ใกล้สุดใน Industrials | 22 Jul 2026 |
| Q4 | **V0 fixture scope:** 144 themes หรือ subset? | ✅ **ใช้ทั้งหมด** — 143 themes (หลังรวม TH-104) ทั้งหมดใช้ใน V0 fixtures | 22 Jul 2026 |

---

## 9. Decision Status

| Decision | Status |
|---|---|
| **DR-005 — Controlled Theme Set** | ✅ **APPROVED** (Founder review 22 Jul 2026) |
| **TH-001 through TH-143** | All 143 Approved — TH-104 merged into TH-082 |

---

## Amendment History

| Date | Change | Authority |
|---|---|---|
| 21 July 2026 | v0.1 — 3 synthetic themes | Gate B Authorization (Founder Decision #17) |
| 21 July 2026 | v0.2 — 11 broad Finviz Sectors (rejected — too broad) | "" |
| 21 July 2026 | v0.3 — 40 Finviz sub-themes from dropdown CSV (rejected — wrong source) | "" |
| 21 July 2026 | v0.4 — 144 Finviz Industries from `docs/finviz.csv` Industry column; ETF/Fund/Shell filtered | "" |
| 22 July 2026 | v1.0 — Founder review complete: Q1 lifecycle confirmed, Q2 Approach C (Stock-First + Theme Enrichment), Q3 TH-104 merged into TH-082, Q4 all 143 themes approved. Gate B COMPLETE. | Founder Decision DR-005 |
