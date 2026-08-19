# QAD-M4B PIT Fixture Specification

> **Status:** DRAFT (AWAITING M4A FREEZE GATE)
> **Authority:** FD #133; M4B Evaluation Contract §3
> **Schema:** Per M4B Evaluation Contract §3.2
> **Total Fixtures:** 10 (minimal coverage for M4B)

---

## Fixture 1: True Temporary Impairment

### Description
A genuinely high-quality business that suffers a temporary headwind, then recovers fully within 2-4 years. The PIT question is whether the system correctly identifies the impairment as temporary and maintains a quality-positive verdict despite near-term price/narrative damage.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-001` |
| **Company** | SBUX — Starbucks Corporation |
| **AS_OF Date** | `2020-04-01` |
| **Fixture Type** | `TEMPORARY` |

### Company Selection Criteria
- Proven durable competitive advantage (brand, store economics, supply chain moat)
- Multi-decade track record of returns on capital >15%
- COVID-19 lockdowns created a severe same-store-sales decline in Q1/Q2 2020
- Balance sheet was sound entering the crisis (investment-grade debt, manageable leverage)
- Store footprint was an asset, not a liability — drive-through and mobile order infrastructure existed

### Evidence Allowed (Pre-AS_OF)
- Pre-COVID financials (FY2015–FY2019): revenue growth, margins, ROIC, store count
- Historical same-store sales trends before COVID
- Pre-pandemic balance sheets, debt maturity schedules, liquidity position
- Qualitative evidence: brand strength, competitive position vs Dunkin' / local coffee chains, customer loyalty program scale
- China expansion evidence through FY2019
- Industry evidence: coffee consumption trends, specialty coffee market growth
- Pre-pandemic analyst reports (dated before 2020-03-01)

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Any Q2/Q3 2020 earnings reports showing recovery
- Any same-store sales improvement data after April 2020
- Any news about vaccine development, reopening timelines, or government stimulus effectiveness post-2020-04-01
- Any analyst upgrades or price target increases post-crash
- Evidence of drive-through or mobile-order resilience during lockdowns
- Any 2021+ financial results showing margin normalization
- Any narrative about "revenge spending" or post-pandemic coffee demand surge

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** Starbucks has a durable competitive advantage rooted in brand equity, store network effects, and supply chain scale | **HIGH** — multiple pre-AS_OF sources support this over decades |
| **H2:** The COVID-19 lockdowns created a temporary revenue impairment that does not damage the economic moat | **HIGH** — evidence of pre-crisis strength and temporary nature of lockdowns |
| **H3:** Starbucks' balance sheet is adequate to survive a 12-18 month revenue disruption without restructuring | **HIGH** — pre-AS_OF investment-grade debt, manageable leverage, liquidity lines |
| **H4:** The impairment is structural — consumer habits shift permanently away from out-of-home coffee | **LOW** — no pre-AS_OF evidence supports permanent habit shift; limited historical precedent |
| **H5:** Valuation at the AS_OF date prices in a permanent loss scenario that is not justified by fundamentals | **MEDIUM** — depends on price context; plausible but requires valuation analysis |

### Expected Quality State
`VERIFIED` — Starbucks is a genuinely high-quality business by every pre-AS_OF measure.

### Expected Impairment
`TEMPORARY` — The COVID-19 lockdown is a textbook temporary headwind affecting a sound business.

### Expected Verdict
`QAD_CONFIRMED` — System should confirm this as a quality business with temporary impairment.

### Known Outcome Window
`[2021-01-01, 2022-12-31]` — Recovery was visible in earnings by late 2020 and confirmed by 2021-2022 financials.

### Ambiguity Notes
- The severity and duration of COVID-19 was unprecedented; no exact historical analog exists for lockdown enforcement
- Some urban-located stores (financial districts, transit-adjacent) faced permanent demand shifts due to remote work — this is a partial ambiguity but minority of total store base
- China recovery timing was uncertain: Starbucks China recovered faster than US in 2020, but pre-AS_OF evidence could not have predicted the different regional trajectories

---

## Fixture 2: True Structural Deterioration

### Description
A business model permanently destroyed by technological disruption. The economic moat was genuine but the moat was rendered obsolete by a structural change that no defensible strategy could overcome.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-002` |
| **Company** | YELP — Yelp Inc. (or alternately: Yellow Pages / print classifieds declining to irrelevance) |
| **AS_OF Date** | `2015-06-01` |
| **Fixture Type** | `STRUCTURAL` |

### Company Selection Criteria
- Once-dominant business model in a specific information intermediary role
- Clear moat (local advertiser relationships, brand, directory lock-in) that was genuine at its peak
- Disruption visible at AS_OF date: mobile app alternatives, user-generated reviews, self-serve digital advertising
- Revenue decline was already underway but magnitude of permanent loss was not yet fully priced
- No plausible pivot or recovery strategy existed that could restore the old economics
- Note: using Yellow Pages / print classifieds or a similar directory business with clear structural decline

### Evidence Allowed (Pre-AS_OF)
- Historical revenue and margin trends showing decline from peak
- Evidence of digital disruption: smartphone adoption rates, Google Local / Facebook / Craigslist market share gains
- Management commentary about secular headwinds (filings, earnings calls before AS_OF)
- Analyst reports discussing digital substitution risk
- Business model economics: declining listings, shrinking print directories, falling ad rates
- Evidence about competitors' free digital offerings disrupting the paid-model

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Any evidence of successful pivot or restructuring after 2015
- Any eventual bankruptcy filing or liquidation outcome
- Evidence of remaining value extracted in later years
- Post-AS_OF data about the pace of digital advertising migration
- Any 2016+ evidence about the company's eventual survival strategy or failure

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** The business has a genuine but narrow moat based on local advertiser lock-in and brand recognition | **MEDIUM** — moat was real but eroding at AS_OF date |
| **H2:** Digital substitution of print/local directories is a structural change that permanently destroys the business model | **HIGH** — evidence of accelerating digital ad spend shift, free alternatives gaining traction |
| **H3:** The balance sheet provides a limited runway that does not change the structural trajectory | **MEDIUM** — depends on debt levels; temporary cash flows may mask permanent decline |
| **H4:** Cost restructuring or digital pivot could preserve some franchise value | **LOW** — structural nature of disruption makes full recovery implausible; digital pivot attempts at AS_OF date showed limited traction |
| **H5:** At current valuation, equating price decline to potential recovery opportunity is a value trap | **HIGH** — structural decline businesses often appear cheap on traditional multiples before further deterioration |

### Expected Quality State
`FAILED` — The moat is genuinely being destroyed by structural forces.

### Expected Impairment
`STRUCTURAL` — The business model damage is permanent and not recoverable.

### Expected Verdict
`NOT_QAD_STRUCTURAL` — Quality was real but is being structurally destroyed; the verdict excludes this from QAD opportunity set.

### Known Outcome Window
`[2016-01-01, 2020-12-31]` — Continued revenue decline, eventual restructuring or sale at distressed price.

### Ambiguity Notes
- Some print-to-digital transitions succeeded (e.g., Schibsted in Scandinavia, some newspaper transitions); the fixture relies on the specific conditions where transition failed
- The AS_OF date is deliberately early enough that a value-investor case could be made — the ambiguity tests whether the system distinguishes genuine temporary from structural
- A small residual value (e.g., real estate, brand licensing) may remain even after structural impairment — the fixture tests whether the system correctly identifies that this residual does not constitute a quality recovery

---

## Fixture 3: Mixed Impairment

### Description
A multi-business company where some segments face genuine structural damage while others retain intact competitive advantage. The impairment is real but not uniform — the evaluation question is whether the system can disentangle segment-level quality.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-003` |
| **Company** | GE — General Electric (pre-restructuring) |
| **AS_OF Date** | `2018-01-15` |
| **Fixture Type** | `MIXED` |

### Company Selection Criteria
- Multi-business conglomerate with genuinely different competitive dynamics per segment
- At AS_OF date, GE Power was in structural decline (fossil fuel equipment, overcapacity)
- GE Aviation and Healthcare retained genuine competitive advantage (high barriers, installed base, service revenue)
- GE Capital was a source of contingent liability and balance-sheet risk
- The "mixed" nature was the core analytical challenge — not uniform good or bad
- Pre-AS_OF evidence allowed the separation; post-AS_OF confirmed the specific trajectory

### Evidence Allowed (Pre-AS_OF)
- Segment-level financials (Power, Aviation, Healthcare, Capital) through FY2017
- GE Power: declining orders, overcapacity in gas turbines, renewable energy substitution trends
- GE Aviation: installed base data, LEAP engine orders, service revenue contracts
- GE Healthcare: diagnostic imaging market position, R&D pipeline, competitive dynamics vs Siemens/Philips
- GE Capital: regulatory capital requirements, asset composition, contingent liability disclosures
- Historical ROIC by segment (pre-2018 SEC filings)
- Analyst segment-level valuations and sum-of-the-parts analyses
- Management restructuring plans announced before AS_OF date

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Any 2018+ earnings showing the full extent of Power impairment (e.g., the $22B impairment charge in 2018)
- Any details of the eventual GE breakup or restructuring plan outcomes
- Post-2018 debt downgrades or credit rating changes
- Any COVID-era data affecting Aviation (which was separately impacted)
- Post-2018 evidence about GE Capital's eventual wind-down or sale
- Any knowledge of the 2018+ collapse of GE's stock price and dividend cut

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** GE as a whole possesses a durable competitive advantage from diversification, scale, and cross-segment synergies | **LOW** — pre-AS_OF evidence shows conglomerate discount, limited synergies, and divergent segment trajectories |
| **H2:** GE Power faces structural impairment from fossil-fuel demand decline, overcapacity, and renewable substitution — this damage is permanent | **HIGH** — pre-AS_OF data shows declining orders, competitor overcapacity, and policy shifts toward renewables |
| **H3:** GE Aviation retains a genuine competitive advantage from installed base, aftermarket service, and technology barriers | **HIGH** — pre-AS_OF evidence of long-term service contracts, LEAP engine order book, and high switching costs |
| **H4:** GE Healthcare maintains defensible competitive positions but faces manageable competitive pressure | **MEDIUM** — moat exists but is narrower than Aviation's; Siemens/Philips competition is real |
| **H5:** The valuation at AS_OF date incorrectly prices all segments as if they share the same impairment trajectory | **HIGH** — conglomerate structure masks segment divergence; market tends to undervalue the intact-quality segments |

### Expected Quality State
`PROBABLE` — Quality exists in some segments but needs careful delineation; conglomerate structure complicates the assessment.

### Expected Impairment
`MIXED` — Structural in Power; mostly intact in Aviation and Healthcare.

### Expected Verdict
`QAD_PROBABLE` — Quality exists in the intact segments, but only if the system identifies the segment-level differentiation.

### Known Outcome Window
`[2018-06-01, 2021-12-31]` — GE Power impairments fully materialized; GE Aviation and Healthcare continued generating strong cash flows; eventual breakup plan announced.

### Ambiguity Notes
- The mixed nature of this case is the central difficulty: a system that takes a single-company view (good/bad) will fail regardless of which direction it chooses
- The conglomerate's own accounting and reporting made segment-level analysis harder — the system should identify data limitations
- GE Capital's contingent liabilities created a systemic risk that was not fully segment-specific — this adds a balance-sheet dimension separate from quality assessment
- The known outcome window shows Aviation was later impacted by COVID (2020), which was a separate temporary shock — this should not be confused with the structural Power impairment

---

## Fixture 4: False Quality

### Description
A company that appeared to have a competitive advantage but the moat was an illusion — driven by unsustainable factors, accounting manipulation, or cyclical peak that was mistaken for structural quality.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-004` |
| **Company** | WIR — Wirecard AG |
| **AS_OF Date** | `2018-10-01` |
| **Fixture Type** | `FALSE_QUALITY` |

### Company Selection Criteria
- Market narrative at AS_OF date positioned the company as a high-quality fintech disruptor with genuine moat
- Reported financials showed high growth, high margins, and supposedly defensible payment-processing technology
- Multiple red flags were visible pre-AS_OF: auditor concerns (KPMG special audit ongoing), whistleblower reports, short-seller reports (FT, Zatarra)
- The "quality" was an illusion sustained by accounting fraud and unsustainable growth economics
- Post-AS_OF outcome: total collapse, insolvency, fraud conviction of management

### Evidence Allowed (Pre-AS_OF)
- Public financial statements (2015–2017, interim 2018 reports) — growth rates, reported margins, cash conversion
- Auditor reports and any qualified opinions or special audit findings
- Whistleblower reports and legal proceedings (e.g., Singapore, Philippines office concerns)
- Short-seller reports (Zatarra Research, FT reporting) with specific allegations
- Regulatory filings and BaFin (German regulator) actions
- News reports about third-party acquirer relationships and the "partner model"
- Competitive landscape: genuine payment processors (Adyen, Worldpay) vs Wirecard's model
- Analyst reports — both positive and skeptical pre-AS_OF
- Cash flow vs reported earnings divergence
- Balance sheet: suspicious intangible assets, "escrow" accounts, related-party transactions

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Any evidence of the 2019 FT investigation revelations or the 2020 fraud collapse
- Post-2018 auditor resignations or the eventual KPMG special audit findings
- The 2020 bankruptcy filing or insolvency proceedings
- Post-2019 evidence about missing $2B in trust accounts
- Any post-AS_OF regulatory actions beyond BaFin's known pre-2018 actions
- Post-AS_OF criminal convictions or executive arrests
- Post-2018 short seller reports or follow-up FT articles

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** Wirecard possesses a durable competitive advantage in payment processing technology and a regulated financial infrastructure | **LOW** — pre-AS_OF evidence raises substantial doubts: third-party-dependent model, suspicious geography of revenues, opaque partner economics |
| **H2:** The company's reported growth and margins reflect genuine scale advantages in a growing market | **MEDIUM TO LOW** — reported metrics are exceptional but cash conversion, auditor skepticism, and whistleblower allegations create serious questions |
| **H3:** The partner/acquirer model creates a defensible distribution moat that competitors cannot replicate | **LOW** — pre-AS_OF evidence suggests the partner model was a black box where revenue could not be verified |
| **H4:** Red flags in the financial statements (suspicious intangibles, working capital patterns, audit issues) suggest the quality narrative is not supported by underlying economics | **HIGH** — multiple pre-AS_OF sources raise structural financial reporting concerns |
| **H5:** The company's valuation implies a quality premium that is not justified by the evidence available at AS_OF date | **HIGH** — valuation multiples at 2018-10-01 priced in a quality business narrative that pre-AS_OF evidence does not support |

### Expected Quality State
`FAILED` — The appearance of quality is not supported by verifiable evidence.

### Expected Impairment
`STRUCTURAL` — The entire business model was based on unsustainable or fraudulent economics.

### Expected Verdict
`NOT_QAD_QUALITY` — Not a quality business; the market perception of quality was an illusion.

### Known Outcome Window
`[2019-01-01, 2020-12-31]` — FT expose (Jan 2019), KPMG audit refuses to sign off (April 2020), insolvency (June 2020).

### Ambiguity Notes
- The central ambiguity challenge: Wirecard had genuine payment-processing operations (even if smaller than reported) — the system must determine whether the moat was real but smaller, or entirely illusory
- The AS_OF date is before the definitive fraud reveal but after substantial red flags were documented — this tests whether the system weights ambiguous negative evidence appropriately
- False-Quality cases require the system to distinguish "difficult-to-verify" from "verified-as-fraud"; the system must not require certainty to lower quality assessment

---

## Fixture 5: Balance-Sheet Trap

### Description
A genuinely high-quality business that holds significant value but carries leverage or refinancing risk that turns a temporary shock into a permanent loss of equity value. The quality assessment is correct; the impairment diagnosis requires the balance-sheet dimension.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-005` |
| **Company** | HTZ — Hertz Global Holdings (pre-bankruptcy) |
| **AS_OF Date** | `2020-02-01` |
| **Fixture Type** | `BALANCE_SHEET` |

### Company Selection Criteria
- Genuine operational strengths: fleet management expertise, airport concession positions, Hertz-brand recognition, insurance and ancillary revenue streams
- High fixed-cost structure and substantial debt (auto fleet ABS, corporate debt)
- At AS_OF date, the underlying rental car business had genuine economic characteristics (high barriers at airport concessions, fleet purchasing power)
- The balance sheet was structured such that a moderate revenue disruption could trigger covenant breaches and insolvency
- The trap: high business quality + high leverage = equity wiped out even though the operating business survived

### Evidence Allowed (Pre-AS_OF)
- Pre-2020 financial statements showing operating margins, fleet utilization, revenue per unit
- Debt structure: ABS notes, corporate bonds, credit facilities, maturities
- Fleet ownership vs financing breakdown — residual value risk exposure
- Airport concession agreements and competitive position vs Avis/Budget, Enterprise
- Historical performance through prior cycles (2008-09) showing operating resilience
- Management commentary about leverage targets, fleet strategy
- Analyst reports on capital structure risk pre-pandemic
- Credit ratings and debt covenant terms
- Insurance revenue stream characteristics (high-margin, recurring)

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Any evidence of COVID-19 travel demand collapse starting March 2020
- Hertz's eventual bankruptcy filing (May 2020)
- Post-AS_OF fleet impairment charges or vehicle residual value declines
- Any evidence of the eventual restructuring plan or equity wipeout
- Post-February 2020 rental demand data
- Post-AS_OF credit rating downgrades triggered by pandemic
- The 2020 CARES Act or any government pandemic relief programs

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** Hertz has a genuine operational moat from airport concession positions, fleet scale, and brand recognition in the rental car industry | **HIGH** — pre-AS_OF evidence shows durable advantages: concession contracts are long-term and difficult to replicate |
| **H2:** The balance sheet carries material refinancing risk due to the structure and maturity profile of the debt | **HIGH** — pre-AS_OF leverage was disclosed; ABS structures create contingent liability from fleet residual values; debt maturity wall visible at AS_OF date |
| **H3:** Even a moderate, temporary revenue decline could trigger a liquidity crisis that wipes out equity despite operational quality | **MEDIUM** — this is the trap mechanism: the system must model the interaction between operating leverage and financial leverage |
| **H4:** The company's asset base (fleet) provides a safety net that will support debt service and preserve equity value | **LOW TO MEDIUM** — fleet residual value is not protection; it declines with the same shock that impairs revenue, and ABS structures ring-fence cash flows |
| **H5:** At the AS_OF date valuation, the market is correctly pricing balance-sheet risk that is independent of operating quality | **MEDIUM** — the pre-pandemic valuation likely reflected leverage but did not fully price a scenario of severe demand shock |

### Expected Quality State
`VERIFIED` — The operating business meets quality criteria — the assessment must separate operating quality from capital-structure risk.

### Expected Impairment
`MOSTLY_TEMPORARY` — The operating impairment would have been temporary, but the balance sheet structure transformed it into permanent equity loss.

### Expected Verdict
`NOT_QAD_VALUATION` — Quality is genuine but the entry point must account for balance sheet risk; the equity outcome is driven by leverage, not quality failure.

### Known Outcome Window
`[2020-03-01, 2020-12-31]` — Travel demand collapsed March 2020; Hertz filed Chapter 11 May 2020; emerged 2021 with equity wiped out; operating business continued under new ownership.

### Ambiguity Notes
- The core analytical challenge: balance-sheet traps require the system to separate quality assessment from capital-structure analysis — a system that conflates "good business" with "good investment" will miss the trap
- The balance-sheet risk was knowable pre-AS_OF but depended on stress-test modeling — the fixture tests whether the system models leverage scenarios independently of quality
- Some high-leverage companies survived (e.g., Avis had similar leverage but different fleet ownership structure); the system should identify the specific structural features that made Hertz vulnerable
- The post-AS_OF recovery of the operating business under new ownership confirms quality but does not help the equity holder — the system must identify that quality alone does not guarantee equity return

---

## Fixture 6: Industry / Cycle Shock

### Description
An industry-wide dislocation that tests whether the system can distinguish company-specific quality from industry-wide cyclical damage. The impairment is real and severe but industry-driven — the system must identify the company-level competitive advantage within the industry context.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-006` |
| **Company** | CVX — Chevron Corporation |
| **AS_OF Date** | `2014-12-01` |
| **Fixture Type** | `INDUSTRY_SHOCK` |

### Company Selection Criteria
- Major integrated oil and gas company with diversified asset base (upstream, downstream, chemicals)
- Oil price crash of mid-2014 created industry-wide margin collapse and asset impairment
- Chevron had genuine competitive advantages vs peers: low-cost position in Permian, integrated model, investment-grade balance sheet, dividend history
- The crash was industry-wide — the evaluation question is whether the system separates Chevron-specific quality from the oil price cycle
- Known outcome: oil prices partially recovered by 2017-2018; Chevron survived and maintained competitive position; some peers (e.g., weaker E&Ps) did not survive

### Evidence Allowed (Pre-AS_OF)
- Pre-2014 financial statements through Q3 2014
- Oil price history and industry supply/demand dynamics pre-crash
- Chevron's cost structure vs peers (producing cost per barrel, finding & development costs)
- Asset portfolio: major projects (Gorgon LNG, Wheatstone, Permian position) and their economics
- Balance sheet strength: debt ratio, interest coverage, dividend track record
- Downstream and chemicals segment cash flow stability during previous cycles
- Historical performance through 2008-09 oil price decline
- Analyst relative positioning reports
- Reserves replacement ratio and reserve life index

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Any oil price recovery trajectory data after Dec 2014
- Any post-2014 earnings reports showing actual impairment charges or write-downs
- Evidence of OPEC production decisions or supply management post-2014
- Post-2014 data about Chevron's specific project outcomes (Gorgon LNG startup delays, etc.)
- Post-AS_OF competitor analysis showing which weaker peers failed
- Any 2015+ dividend sustainability data

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** Chevron possesses a durable competitive advantage from its low-cost asset base, integrated model, and financial strength relative to industry peers | **HIGH** — pre-AS_OF evidence shows superior cost position, diversified cash flow streams, and stronger balance sheet than most peers |
| **H2:** The impairment is primarily driven by industry-wide oil price decline, not company-specific quality deterioration | **HIGH** — the oil price crash was exogenous and industry-wide; pre-AS_OF evidence shows Chevron's operational metrics were stable through the start of the decline |
| **H3:** The industry shock may be cyclical — oil prices historically recover, and a low-cost producer should survive and potentially gain market share during the downturn | **MEDIUM** — historical oil price cycles support recovery; the system should note the uncertainty (duration and magnitude of the price decline unknown at AS_OF date) |
| **H4:** Chevron's balance sheet is strong enough to sustain the dividend and capital program through a multi-year downturn | **MEDIUM** — pre-AS_OF financial strength is evident but the duration of the downturn was the unknown variable |
| **H5:** The market at AS_OF date is pricing industry-wide distress and not distinguishing Chevron's relative quality advantage | **MEDIUM** — industry-wide selloffs often undervalue high-quality operators within the industry |

### Expected Quality State
`VERIFIED` — Chevron demonstrates genuine competitive advantages within the oil and gas industry.

### Expected Impairment
`TEMPORARY` (cyclical industry shock, not permanent quality destruction).

### Expected Verdict
`QAD_PROBABLE` — Quality is intact; industry shock is likely cyclical; the company's relative position may strengthen in the downturn.

### Known Outcome Window
`[2017-01-01, 2020-01-01]` — Oil prices recovered to $50-70 range by 2017-18; Chevron maintained dividend and resumed capital investment; relative outperformance vs weaker peers confirmed.

### Ambiguity Notes
- The key test: the system must not conflate industry-wide distress with company-level quality deterioration — this is a common Type A failure mode
- The oil and gas industry has structural headwinds (energy transition) that were visible at the AS_OF date but less certain — the fixture tests whether the system can distinguish cyclical from secular within one industry
- Chevron's relative quality is shown through comparison with peers (Apache, OXY, COP) not through absolute statements — the system should use comparative evidence

---

## Fixture 7: Company-Specific Shock

### Description
A company-specific event that severely damages the business but is temporary and addressable. The impairment is isolated to a particular product, market, or management issue — not a structural quality failure.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-007` |
| **Company** | BA — Boeing Company |
| **AS_OF Date** | `2019-04-01` |
| **Fixture Type** | `COMPANY_SHOCK` |

### Company Selection Criteria
- Dominant competitive position in commercial aerospace (duopoly with Airbus)
- High barriers to entry (scale, certification, IP, supply chain relationships)
- Company-specific shock: 737 MAX grounding after two fatal crashes (Lion Air Oct 2018, Ethiopian Airlines Mar 2019)
- The shock was severe (production halt, delivery stop, reputational damage, regulatory risk) but the underlying competitive structure of the industry was intact
- Known outcome: 737 MAX returned to service after recertification; Boeing's market position persisted (though not undamaged)
- The question: is this a quality impairment or a (manageable) company-specific crisis within a still-defensible moat?

### Evidence Allowed (Pre-AS_OF)
- Pre-grounding financial statements (2014–2018): revenue, margins, backlog, delivery trends
- Backlog composition and duration: commercial aircraft orders, defense contracts
- Duopoly dynamics: Boeing vs Airbus market share history, production rates
- Certification and regulatory environment pre-grounding
- 737 program economics: production costs, margins, supplier contracts
- Defense & Space segment diversification cash flow
- Services segment revenue and growth trajectory
- Management and engineering culture evidence (pre-crisis)
- Historical precedent: Boeing's recovery from 787 battery crisis (2013), DC-10 grounding (1979)
- Industry barriers: capital requirements, certification costs, customer switching costs

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Any evidence of 737 MAX recertification timeline or approval (return to service in Nov 2020)
- Any FAA or international regulatory decisions after April 2019
- 737 MAX production restart dates or delivery resumption data
- COVID-19 impact on aerospace demand (post-March 2020)
- Post-2019 financial impacts: customer compensation settlements, production cost increases from the grounding
- Any post-AS_OF management changes or restructuring outcomes
- Post-AS_OF MAX crash investigation final reports or legal settlements

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** Boeing possesses a durable competitive advantage from the commercial aerospace duopoly, barriers to entry, installed base lock-in, and customer switching costs | **HIGH** — pre-AS_OF evidence strongly supports the duopoly structure and industry barriers; the competitive position is not quickly replicable |
| **H2:** The 737 MAX grounding is a company-specific shock that does not destroy the underlying industry structure or Boeing's position within it | **HIGH** — the shock is severe but industry structure evidence (Airbus capacity constraints, airline switching costs, certification barriers) supports recovery |
| **H3:** Boeing's quality assessment should be downgraded due to the safety and engineering failures that caused the MAX crisis | **MEDIUM** — the event reveals genuine quality concerns (engineering culture, regulatory relationship management) but does not destroy the moat |
| **H4:** The shock could become structural if regulatory trust is permanently lost or if airlines permanently shift orders to Airbus | **LOW TO MEDIUM** — pre-AS_OF evidence shows Airbus was at full production capacity and could not absorb Boeing's backlog; regulatory relationships can recover over time |
| **H5:** At AS_OF date valuation, the market is pricing the MAX crisis as if it were a permanent impairment | **MEDIUM** — price damage was severe but the structural case for recovery is evidence-based |

### Expected Quality State
`PROBABLE` — Quality is real but the event reveals genuine weaknesses in execution/engineering culture.

### Expected Impairment
`MOSTLY_TEMPORARY` — The core moat survives; some long-term position damage (market share loss to Airbus, compensation costs) is probable.

### Expected Verdict
`QAD_PROBABLE` — Quality is intact enough to justify inclusion; the impairment is primarily temporary with some permanent position loss.

### Known Outcome Window
`[2020-11-01, 2023-12-31]` — 737 MAX returned to service Nov 2020; deliveries resumed gradually; Boeing maintained duopoly position but lost some market share; additional quality issues (2024 door plug) separate from the evaluation period.

### Ambiguity Notes
- The distinction between "temporary shock to a quality business" and "the shock reveals the business was never high quality" is the central ambiguity — the 737 MAX revealed engineering and safety culture problems that had been latent for years
- Boeing's defense segment provides a meaningful diversification buffer that was intact throughout the crisis
- The COVID-19 pandemic (which was unknowable at the AS_OF date) later created a second, separate demand shock that compounded the MAX crisis — the PIT evaluation must not conflate these

---

## Fixture 8: Unresolved / Ambiguous Case

### Description
A genuinely ambiguous situation where the available evidence at the PIT date supports competing interpretations. The evaluation tests whether the system can properly express uncertainty and articulate both sides of the argument — not reach a forced verdict.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-008` |
| **Company** | TSLA — Tesla, Inc. |
| **AS_OF Date** | `2018-06-01` |
| **Fixture Type** | `AMBIGUOUS` |

### Company Selection Criteria
- At the AS_OF date, Tesla had achieved significant product-market fit (Model 3 production ramp underway)
- Multiple competing narratives were supportable with pre-AS_OF evidence:
  - Narrative A: Tesla had a genuine and durable moat in EV technology, battery cost, brand, and charging infrastructure
  - Narrative B: Tesla's advantages were temporary — incumbent OEMs would catch up, margins were unsustainable, demand was lumpy
- The company was financially fragile (negative free cash flow, debt maturities, no GAAP profitability) but operationally disruptive
- The ambiguity was genuine and unresolved — both sides had reasonable evidence
- Known outcome window is partial — the case is still unfolding in some dimensions

### Evidence Allowed (Pre-AS_OF)
- Pre-2018-06 financials: revenue trajectory, gross margins (including regulatory credit contribution), operating cash flow
- Model 3 production ramp data: weekly production rate, bottlenecks, quality issues
- Battery cost trajectory and Gigafactory capacity
- Supercharger network scale and competitive moat
- Competitive landscape: incumbent OEM EV commitments (VW, GM, Nissan, etc.), production timelines, model announcements
- Regulatory environment: ZEV credits, emissions standards, EV mandates
- Brand strength: consumer surveys, reservation data, customer satisfaction indicators
- Management credibility and execution track record against prior targets
- Capital structure: debt maturity schedule, convertible bond terms, equity dilution history
- Autopilot/FSD development status and regulatory pathway uncertainty

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Post-2018-06 production and delivery data showing sustained volume growth
- Any evidence of sustained GAAP profitability achieved (from Q3 2019 onward)
- Post-2018 stock price trajectory, valuation multiples, or market capitalization
- Post-2018 competitive product launches or incumbent OEM EV program outcomes
- Post-2018 battery technology developments (4680 cells, etc.)
- 2020+ evidence about Tesla's market share in EVs or overall automotive market
- China Gigafactory completion timeline and output data

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** Tesla possesses a durable competitive advantage from battery cost leadership, charging infrastructure, brand, and software/autonomy | **MEDIUM** — evidence supports this but also raises questions about sustainability and incumbent competition |
| **H2:** Tesla's advantages are temporary — incumbent OEMs will replicate EV technology, Tesla's cost advantage will erode, and brand alone is not a durable moat | **MEDIUM** — evidence of incumbent investments and Tesla's execution risk supports this; but incumbent track record in catching up is unproven at AS_OF date |
| **H3:** The financial fragility (negative FCF, debt, execution risk) means that even a quality business may not survive to capture the value | **MEDIUM TO HIGH** — the balance sheet and cash burn were real concerns; the ambiguity is whether financial fragility offsets operational advantage |
| **H4:** The pessimistic case is more likely — Tesla is a temporarily disruptive company that will settle into an ordinary automotive industry position | **LOW TO MEDIUM** — defensible argument but weaker than the competing narratives given pre-AS_OF evidence |
| **H5:** No verdict can be reached with high confidence — the available evidence supports multiple interpretations and the system should express calibrated uncertainty | **HIGH** — this is the core test: can the system express ambiguity rather than forcing a verdict? |

### Expected Quality State
`UNRESOLVED` — Genuine ambiguity prevents a quality verdict with high confidence.

### Expected Impairment
`UNRESOLVED` — Cannot determine whether competitive advantages are durable or temporary.

### Expected Verdict
`QAD_UNRESOLVED` — The system should flag this as a watch case requiring evidence progression before a verdict.

### Known Outcome Window
`[2019-01-01, 2025-12-31]` — Partial: Tesla achieved GAAP profitability (2019-2020), sustained volume growth, and dominant EV market share; valuation and competitive durability remain debated.

### Ambiguity Notes
- This is the hardest fixture type for most systems because LLMs are trained to produce confident outputs — the evaluation tests whether the system can resist forced verdicts
- The ambiguity is structural: the company is simultaneously operationally impressive and financially fragile — a system that only looks at one dimension will produce an overconfident result
- The known outcome window is intentionally partial — the long-term quality question (will Tesla's moat persist vs incumbent competition?) is still unresolved as of the writing of this spec
- The system must demonstrate explicit calibration: articulate confidence levels, identify what evidence would resolve the ambiguity, and recommend monitoring parameters

---

## Fixture 9: Valuation Failure

### Description
Severe price decline driven by mistaken market perception of permanent impairment when the underlying business quality is intact. The market was wrong — the business recovered and the price decline was a buying opportunity. Tests whether the system can separate valuation from quality.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-009` |
| **Company** | AMZN — Amazon.com, Inc. |
| **AS_OF Date** | `2000-12-01` |
| **Fixture Type** | `VALUATION_FAILURE` |

### Company Selection Criteria
- Amazon was a genuinely high-growth, high-quality business even at the 2000 dot-com peak
- The 2000 tech crash crushed Amazon's stock price (~90% decline from peak)
- The market narrative at the time: Amazon was a "dot-com bust" with no path to profitability — the burn rate was unsustainable
- The market was wrong: Amazon's business model (e-commerce infrastructure, third-party marketplace, AWS-not-yet-known) had genuine competitive advantage that the price did not reflect
- Amazon's retail business was genuinely high-quality (customer experience, selection, logistics scale)
- The valuation failure: market priced permanent impairment where only temporary (or even non-existent) impairment existed
- Known outcome: Amazon survived, thrived, and became one of the most valuable companies in the world

### Evidence Allowed (Pre-AS_OF)
- Pre-2000 financials through Q3 2000: revenue growth trajectory, gross margin trends (improving through own sales + marketplace)
- Customer metrics: repeat purchase rates, customer satisfaction scores, Prime launch (2005 — note: NOT allowed, it's post-AS_OF)
- Wait — Prime (2005) is post-AS_OF. The evidence period is pre-2000-12-01.
- Valid pre-AS_OF evidence: retail execution, selection expansion, logistics build-out, early marketplace (launched 2000)
- Cash position and burn rate: disclosed in filings
- Business model fundamentals: negative working capital model (pay suppliers after collecting from customers)
- Competitive landscape: Barnes & Noble, Borders, early e-commerce competition
- Analyst reports from the period (both bullish and bearish)
- Early evidence of marketplace economics (higher margin, asset-light)
- Bezos' shareholder letters and strategic communications

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Any evidence of Amazon achieving profitability (2001+) or subsequent years
- AWS launch (2006) or cloud computing market
- Prime subscription program success (2005 onwards)
- Marketplace growth trajectory post-2000
- Stock price recovery after 2001 (any trading data after Dec 2000)
- Any evidence of competitors failing (Borders bankruptcy 2011, etc.)
- Post-2000 metrics: revenue growth, margin expansion, cash flow generation
- Any evidence that Amazon became the dominant global e-commerce platform

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** Amazon has a competitive advantage in e-commerce from customer experience, selection, and logistics infrastructure that is improving relative to competitors | **MEDIUM TO HIGH** — pre-AS_OF evidence shows accelerating revenue, expanding selection, negative working capital advantages, and improving customer metrics |
| **H2:** Amazon's business model will lead to structural profitability that is not reflected in the current market price | **MEDIUM** — the path to profitability was uncertain at AS_OF date but the working capital model and marketplace launch provide a plausible mechanism |
| **H3:** The impairment is permanent — Amazon is a fundamentally unprofitable business model with no path to meaningful returns | **LOW** — pre-AS_OF evidence does not support this thesis; the negative working capital model, improving gross margins, and marketplace launch contradict the burn-rate narrative |
| **H4:** The severe price decline at AS_OF date reflects market panic about a business model that has demonstrable quality characteristics | **MEDIUM TO HIGH** — the disconnect between price damage and improving operational metrics is evident from pre-AS_OF data |
| **H5:** Amazon's competitive position may actually strengthen during the downturn as weaker e-commerce competitors fail | **MEDIUM** — dot-com crash eliminated many e-commerce competitors; pre-AS_OF evidence of Amazon's relative financial position (cash reserves, revenue growth) supports this |

### Expected Quality State
`VERIFIED` — Amazon's business demonstrated genuine quality characteristics even at the depth of the dot-com crash.

### Expected Impairment
`TEMPORARY` (or minimally, `MOSTLY_TEMPORARY` — the impairment narrative was wrong; the business was never structurally impaired).

### Expected Verdict
`QAD_CONFIRMED` — Quality business with no structural impairment; the price decline was a valuation failure driven by market narrative, not company fundamentals.

### Known Outcome Window
`[2001-01-01, 2005-12-31]` — Amazon reached profitability (2001 holidays); achieved $8B+ revenue by 2005; stock recovered steadily from 2001 lows.

### Ambiguity Notes
- The key test: the system must not use post-AS_OF knowledge (AWS, Prime, eventual dominance) in its PIT assessment — the evidence available at December 2000 was genuinely mixed on profitability timing
- The valuation failure concept requires the system to express: "the business is high quality; the price implies otherwise; the quality evidence is more reliable than the price signal"
- At the AS_OF date, some legitimate concerns existed: cash burn was real, profitability was not guaranteed, and Amazon's model was unproven at scale — the fixture tests whether the system can acknowledge these concerns while still reaching a quality-positive conclusion
- The distinction from Narrative Panic (Fixture 10): Valuation Failure involves a real business whose intrinsic quality is misunderstood; Narrative Panic involves a price decline far exceeding even worst-case economic damage

---

## Fixture 10: Narrative Panic

### Description
A severe price decline driven by panic/fear that far exceeds even a reasonable worst-case assessment of economic damage. The price damage is orders of magnitude larger than what the underlying fundamental impairment could justify.

| Field | Value |
|-------|-------|
| **Fixture ID** | `FIX-2026-010` |
| **Company** | AAPL — Apple Inc. |
| **AS_OF Date** | `2013-04-01` |
| **Fixture Type** | `NARRATIVE_PANIC` |

### Company Selection Criteria
- Apple had demonstrated genuine competitive advantage: ecosystem lock-in (hardware + software + services), brand, customer loyalty, supply chain mastery
- Pre-2013 period saw significant price decline (~45% from Sep 2012 peak to Apr 2013)
- The narrative at AS_OF date: "Apple is doomed without Steve Jobs — innovation is dead, iPhone market is saturated, competition (Samsung) is winning, margins are collapsing"
- The narrative-driven price decline exceeded what reasonable fundamental analysis would suggest
- Apple's actual business at AS_OF date: massive installed base, high customer retention, growing services revenue (App Store, iTunes), strong balance sheet with $150B+ cash
- Known outcome: Apple recovered to become the most valuable company in the world; the "innovation is dead" narrative was wrong
- Key distinction from Valuation Failure (Amazon 2000): Apple was already highly profitable, had massive cash reserves, and was generating enormous free cash flow — the price decline was purely narrative/panic-driven, not about profitability survival

### Evidence Allowed (Pre-AS_OF)
- Pre-2013 financials through March 2013: revenue, gross margins, net income, free cash flow
- Installed base: iPhone, iPad, Mac active user metrics
- Ecosystem evidence: App Store revenue, developer count, customer switching costs, platform lock-in
- Customer satisfaction and loyalty survey data
- Balance sheet: cash position, capital allocation history (dividend initiated 2012, buyback program)
- Competitive position: iPhone vs Samsung market share history, smartphone market growth
- Supply chain and manufacturing scale advantages
- Brand value surveys (Interbrand, etc.)
- Management (Tim Cook) operational track record
- Services revenue growth trajectory (pre-2013 visible App Store growth)
- Capital return program announcement (2012-2013)

### Evidence Forbidden (Post-AS_OF — Leak Test Target)
- Any post-2013 stock price recovery data
- Evidence of subsequent product launches (Apple Watch 2015, AirPods 2016, Services growth post-2013)
- iPhone 6 success and the "super cycle" (2014-2015)
- Post-2013 market capitalization reaching $1T+ (2018)
- Any post-2013 services revenue breakout data
- Post-2013 evidence about Samsung's competitive decline or Chinese OEM market dynamics
- Post-2013 dividend increases or buyback acceleration outcomes
- Post-2013 customer metrics showing sustained or improving satisfaction

### Expected Hypotheses (H1–H5)

| Hypothesis | Expected Plausibility |
|-----------|----------------------|
| **H1:** Apple possesses a durable competitive advantage from ecosystem lock-in, brand, customer switching costs, and platform economics | **HIGH** — pre-AS_OF evidence strongly supports this: high customer retention, growing App Store, premium brand positioning, unparalleled supply chain |
| **H2:** The "Apple is doomed without Jobs" narrative is not supported by the evidence — the competitive position at AS_OF date is intact and improving | **HIGH** — operational metrics (revenue, margins, customer satisfaction, installed base growth, services trajectory) do not support a structural decline thesis |
| **H3:** iPhone market may be approaching saturation, but this is a deceleration not a structural impairment — installed base moat increases with cumulative sales | **MEDIUM TO HIGH** — saturation concerns are valid but installed base lock-in is a unique competitive advantage; upgrade cycle and services revenue provide a buffer |
| **H4:** The price decline from the Sep 2012 peak far exceeds what any reasonable fundamental scenario would justify — the price narrative is disconnected from business reality | **HIGH** — Apple was generating enormous cash flows with $150B+ cash; a ~45% price decline for a company with these fundamentals is evidence of narrative-driven panic |
| **H5:** The impairment, if any, is a mild deceleration — not a structural quality failure — and the valuation at AS_OF date presents a quality entry point | **HIGH** — the gap between price and fundamental evidence at AS_OF date supports a quality-positive conclusion with high conviction |

### Expected Quality State
`VERIFIED` — Apple's quality and competitive advantages are clearly supported by pre-AS_OF evidence.

### Expected Impairment
`MOSTLY_TEMPORARY` — Some growth deceleration is visible at AS_OF date but does not remotely justify the price decline magnitude.

### Expected Verdict
`QAD_CONFIRMED` — Quality is intact; the narrative-driven panic creates a strong QAD opportunity.

### Known Outcome Window
`[2014-01-01, 2018-12-31]` — Apple stock recovered strongly (iPhone 6 cycle 2014-15, record earnings, services growth); reached $1T market cap in 2018.

### Ambiguity Notes
- The distinction between Valuation Failure (Fixture 9) and Narrative Panic: both involve price declines driven by market misperception, but Narrative Panic involves a clearly profitable, cash-rich company where the price decline has no plausible fundamental basis even at the AS_OF date
- The "Steve Jobs is gone" narrative was intangible and difficult to disprove with evidence — the system should identify that the narrative lacks falsifiable evidence and should be weighted below fundamental data
- Customer switching costs (iCloud lock-in, app purchases, ecosystem compatibility) were knowable at AS_OF date but often underweighted in market narratives
- The fixture tests whether the system can resist high-profile consensus narratives when fundamental evidence contradicts them

---

**END OF PIT FIXTURE SPECIFICATION**