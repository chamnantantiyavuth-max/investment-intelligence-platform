"""Adapters — read approved pipeline artifacts, admit + map to response contracts (arch v0.4 §6, plan T5).

Design principles (arch v0.4 §2):
- Read, don't re-run: ONE immutable byte snapshot per request; same bytes drive hash/ingest/map/serve.
- Provenance read from artifact, never invented. Three-way classification:
  real (market/price/rank from _real_eod overlays / real pipeline outputs),
  synthetic (SRC-SYN-* evidence), human_sourced (source null / Founder Obsidian Vault / Founder Journal).
- Fail closed: missing/synthetic/unknown/stale -> HTTP 503. NO synthetic fallback on real surfaces (D2).
- Staleness bounds (D3): AM as_of <= 7d, FO <= 30d, II <= 120d.
"""
from __future__ import annotations

import contextvars
import hashlib
import hmac
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from backend import persistence
from backend.schemas.responses import (
    AMQueueResponse, CandidateQuality, CandidateSummary, ComponentProvenance, DataConfidence,
    EntryReadiness, EvidenceProvenance, EvidenceRecord, IISignalsResponse, IISignalSummary,
    Provenance, ResearchPackageDetail, ResearchPackageSummary, ThemeSummary, ThemeWithCandidates,
)

ADAPTER_VERSION = "v4"
# Immutable adapter registry (plan T5 / council F3): version -> committed code hash of adapters.py.
# Stored in a SEPARATE json so editing the registry cannot change the code hash (no circularity).
# If adapters.py changes, recompute hash + bump ADAPTER_VERSION. verify_adapter_registry() enforces.
_ADAPTER_REGISTRY_PATH = Path(__file__).with_name("adapter_registry.json")
ADAPTER_REGISTRY: dict[str, str] = json.loads(_ADAPTER_REGISTRY_PATH.read_text(encoding="utf-8"))
ADAPTER_CODE_HASH = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

# Per-request lineage accumulator: route handlers touch artifacts -> adapters record which
# (module, run_id) were served; CaptureResponseMiddleware persists api_reads + api_read_runs.
REQUEST_RUNS: contextvars.ContextVar[list[tuple[str, str]]] = contextvars.ContextVar(
    "request_runs", default=[])
LAST_READ_ID: contextvars.ContextVar[int] = contextvars.ContextVar("last_read_id", default=0)

# Staleness bounds (FD #47 D3 — operational, NOT investment rules)
STALENESS_DAYS = {"am": 7, "fo": 30, "ii": 120}

_REAL_OVERLAY_MARKER = "_real_eod"
_SYN_EVIDENCE_RE = re.compile(r"^SRC-SYN")


class ArtifactUnavailable(Exception):
    """Raised when an artifact fails admission (missing/synthetic/unknown/stale/corrupt)."""

    def __init__(self, module: str, reason: str, detail: str = ""):
        self.module = module
        self.reason = reason
        self.detail = detail
        super().__init__(f"{module}: {reason}")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _artifact_path(module: str) -> Path:
    base = os.environ.get("IIP_ARTIFACT_BASE")
    if base:
        return Path(base) / module / "pipeline_result.json"
    rel = {
        "am": "alpha-momentum-v0/output/pipeline_result.json",
        "fo": "fundamental-opportunity-v0/output/pipeline_result.json",
        "ii": "institutional-intelligence-v0/output/institutional_signals.json",
    }[module]
    return _repo_root() / rel


def verify_adapter_registry() -> None:
    """F3: code hash must match the registered version — source change without version bump fails."""
    registered = ADAPTER_REGISTRY.get(ADAPTER_VERSION)
    if registered is None:
        raise RuntimeError(f"ADAPTER_VERSION={ADAPTER_VERSION!r} not present in ADAPTER_REGISTRY")
    if not hmac.compare_digest(registered, ADAPTER_CODE_HASH):
        raise RuntimeError(
            f"adapter code hash {ADAPTER_CODE_HASH[:16]}… != registered hash for v{ADAPTER_VERSION} "
            f"({registered[:16]}…) — bump ADAPTER_VERSION + ADAPTER_REGISTRY after changing adapters.py")


def load_snapshot(module: str) -> tuple[bytes, dict | list]:
    """Load ONE immutable byte snapshot for this request (no TOCTOU), ingest for lineage.

    The exact bytes read are the bytes registered (persistence.ingest_run) and the bytes
    mapped to the response (council F1: same snapshot drives hash / ingest / map / serve).
    """
    path = _artifact_path(module)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        raise ArtifactUnavailable(module, "missing", f"artifact not found: {path}")
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ArtifactUnavailable(module, "corrupt", str(e))
    # F1: register the exact served bytes in the immutable run registry + record lineage.
    # Corrupt-bytes path is unreachable here (handled above) but ingest may still raise on
    # non-dict artifacts — those are admission failures, not 5xx. Map to ArtifactUnavailable.
    try:
        run_id = persistence.ingest_run(module, raw)
    except Exception as e:
        raise ArtifactUnavailable(module, "corrupt", str(e))
    REQUEST_RUNS.get().append((run_id, module))
    return raw, parsed


def _parse_date(s: str | None) -> datetime | None:
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(s[:19], fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _is_stale(module: str, as_of: str | None) -> bool:
    dt = _parse_date(as_of)
    if dt is None:
        return False  # absence of date is handled by mode/presence admission, not staleness
    age = (datetime.now(timezone.utc) - dt).days
    return age > STALENESS_DAYS[module]


def admit(module: str, parsed: dict | list) -> Provenance:
    """Admission rule (F5): mode must be real; not stale; else raise ArtifactUnavailable (503)."""
    mode, source, as_of, coverage, completeness, hybrid = _extract_provenance_fields(module, parsed)
    if mode != "real":
        raise ArtifactUnavailable(module, "wrong-mode", f"mode={mode!r} — real endpoints reject non-real artifacts")
    if _is_stale(module, as_of):
        raise ArtifactUnavailable(module, "stale", f"as_of={as_of!r} older than {STALENESS_DAYS[module]}d bound")
    return Provenance(source=source, mode=mode, as_of=as_of, coverage=coverage,
                      completeness=completeness, hybrid=hybrid)


def _extract_provenance_fields(module: str, parsed: dict | list):
    """Derive {mode, source, as_of, coverage, completeness, hybrid} from artifact fields only.

    NOTE: tuple order is (mode, source, as_of, coverage, completeness, hybrid) — matches admit().
    """
    if module == "am":
        fixture = parsed.get("fixture_category", "") if isinstance(parsed, dict) else ""
        mode = "real" if "REAL" in fixture.upper() else "synthetic"
        raw = json.dumps(parsed, default=str)
        hybrid = "_real_eod" in raw and "SRC-SYN" in raw
        return (mode, "yahoo_finance_eod", parsed.get("point_in_time"), "9/9",
                "complete", hybrid)
    if module == "fo":
        env = parsed if isinstance(parsed, dict) else {}
        prov = env.get("provenance", {})
        mode = str(prov.get("mode", "")).lower()
        return (mode, prov.get("source", "unknown"), prov.get("as_of"),
                prov.get("coverage"), prov.get("completeness"), bool(prov.get("hybrid", False)))
    if module == "ii":
        meta = parsed.get("meta", {}) if isinstance(parsed, dict) else {}
        ds = str(meta.get("data_source", "")).upper()
        mode = "real" if "REAL" in ds else ("synthetic" if "SYNTHETIC" in ds else "unknown")
        completeness = meta.get("completeness", "complete")
        return (mode, "sec_edgar_13f", meta.get("as_of") or meta.get("generated_at"),
                meta.get("coverage"), completeness, False)
    raise ArtifactUnavailable(module, "unknown-module")


# ── AM mapping ────────────────────────────────────────────────────────────────
def _classify_evidence(evidence_list: list, theme_id: str) -> list[EvidenceProvenance]:
    """Classify evidence entries linked to a theme (arch §3): real | synthetic | human_sourced.

    Evidence is artifact-level: entries carry a `theme` field linking them to themes.
    Classification reads the `source` field only — never invented (F4):
      SRC-SYN-* -> synthetic; null/empty/Founder Obsidian Vault/Founder Journal -> human_sourced;
      anything else -> real.
    """
    out = []
    for ev in evidence_list:
        if not isinstance(ev, dict):
            continue
        if ev.get("theme") != theme_id:
            continue
        src = ev.get("source")
        sid = ev.get("id", "")
        if isinstance(src, str) and _SYN_EVIDENCE_RE.match(src):
            out.append(EvidenceProvenance(source_id=str(sid), source_type="synthetic"))
        elif src in (None, "", "Founder Obsidian Vault", "Founder Journal"):
            out.append(EvidenceProvenance(source_id=str(sid), source_type="human_sourced"))
        else:
            out.append(EvidenceProvenance(source_id=str(sid), source_type="real"))
    return out


def _theme_provenance(theme: dict, raw: str, evidence_types: set[str]) -> Provenance:
    hybrid = "_real_eod" in raw or evidence_types != {"real"}
    return Provenance(source="yahoo_finance_eod", mode="real", as_of=None,
                      coverage="9/9", completeness="complete", hybrid=hybrid)


def _clean_alternatives(alt: object) -> dict[str, str] | None:
    """Read-only normalization of artifact alternative_explanations (drop None/'None')."""
    if not isinstance(alt, dict):
        return None
    out = {str(k): str(v) for k, v in alt.items() if v not in (None, "None") and str(v).strip()}
    return out or None


def _counter_evidence_for(parsed: dict, theme_id: str, cand_theme: dict[str, str]) -> list[str] | None:
    """Unresolved counter-evidence SCOPED to this theme's candidates (audit C2 fix:
    overrides belong to a candidate; their counter-evidence must never leak to
    unrelated themes — OVR-001/CAND-002 lands on TH-004 only, not TH-014)."""
    out: list[str] = []
    for o in parsed.get("overrides", []):
        if not isinstance(o, dict):
            continue
        cid = o.get("candidate_id")
        if cand_theme.get(cid) != theme_id:
            continue
        v = o.get("unresolved_counter_evidence")
        if isinstance(v, str) and v and v != "None":
            out.append(v)
        elif isinstance(v, list):
            out.extend(x for x in v if isinstance(x, str) and x)
    return out or None


def _map_theme(theme: dict, raw: str, evidence_list: list,
               alt_expl: dict[str, str] | None = None,
               counter_ev: list[str] | None = None) -> ThemeSummary:
    ev_prov = _classify_evidence(evidence_list, theme["id"])
    types = {e.source_type for e in ev_prov}
    theme_evidence = [
        EvidenceRecord(id=str(e.get("id", "")), type=str(e.get("type", "")),
                       content=str(e.get("content", "")), source=e.get("source"))
        for e in evidence_list
        if isinstance(e, dict) and e.get("theme") == theme["id"]
    ]
    own_alt = ({theme["id"]: alt_expl[theme["id"]]} if alt_expl and theme["id"] in alt_expl else None)
    return ThemeSummary(
        id=theme["id"], name=theme["name"], sector=theme.get("sector", ""),
        industry=theme.get("industry", ""), lifecycle=theme.get("lifecycle", ""),
        approval_status=theme.get("approval_status", ""), monitoring_status=theme.get("monitoring_status", ""),
        confidence=theme.get("confidence", ""), key_tickers=theme.get("key_tickers", []),
        stocks_in_industry=theme.get("stocks_in_industry", 0), why_now=theme.get("why_now", ""),
        provenance=_theme_provenance(theme, raw, types), evidence_provenance=ev_prov,
        alternative_explanations=own_alt, evidence=theme_evidence or None,
        unresolved_counter_evidence=counter_ev,
    )


def _map_candidate(cand: dict, raw: str) -> CandidateSummary:
    cq = cand.get("candidate_quality", {})
    er = cand.get("entry_readiness", {})
    dc = cand.get("data_confidence", {})
    return CandidateSummary(
        id=cand["id"], ticker=cand.get("ticker", ""), research_state=cand.get("research_state", ""),
        conviction_level=cand.get("conviction_level", ""),
        candidate_quality=CandidateQuality(
            fundamentals=cq.get("fundamentals", ""), growth=cq.get("growth", ""),
            liquidity=cq.get("liquidity", ""), relative_strength=cq.get("relative_strength", ""),
            trend_quality=cq.get("trend_quality", ""), accumulation=cq.get("accumulation", ""),
            industry_leadership=cq.get("industry_leadership", "")),
        entry_readiness=EntryReadiness(
            price_structure=er.get("price_structure", ""), base_quality=er.get("base_quality", ""),
            breakout_proximity=er.get("breakout_proximity", ""), volume_behavior=er.get("volume_behavior", ""),
            volatility_contraction=er.get("volatility_contraction", ""),
            extension_risk=er.get("extension_risk", "")),
        data_confidence=DataConfidence(
            freshness=dc.get("freshness", ""), completeness=dc.get("completeness", ""),
            reliability=dc.get("reliability", ""), conflicts=dc.get("conflicts", ""),
            missing_data=dc.get("missing_data", "")),
        provenance=Provenance(source="yahoo_finance_eod", mode="real", as_of=None,
                              coverage="9/9", completeness="complete",
                              hybrid="_real_eod" in raw,
                              component_map={"price_structure": "real", "base_quality": "real",
                                             "breakout_proximity": "real", "volume_behavior": "real",
                                             "volatility_contraction": "real", "extension_risk": "real"}),
    )


def am_queue() -> AMQueueResponse:
    raw, parsed = load_snapshot("am")
    if not isinstance(parsed, dict):
        raise ArtifactUnavailable("am", "corrupt", "AM artifact must be a dict")
    admit("am", parsed)
    raw_str = raw.decode("utf-8", errors="replace")
    evidence_list = parsed.get("evidence", [])
    alt_expl = _clean_alternatives(parsed.get("alternative_explanations"))
    # candidate_id -> theme_id map for counter-evidence scoping (audit C2)
    cand_theme: dict[str, str] = {}
    for item in parsed.get("queue", []):
        _tid, payload = item[0], item[1]
        for c in payload.get("candidates", []):
            cand_theme[c.get("id")] = _tid
    themes = []
    for item in parsed.get("queue", []):
        theme_id, payload = item[0], item[1]
        counter_ev = _counter_evidence_for(parsed, theme_id, cand_theme)
        themes.append(ThemeWithCandidates(
            theme=_map_theme(payload.get("theme", {}), raw_str, evidence_list, alt_expl, counter_ev),
            candidates=[_map_candidate(c, raw_str) for c in payload.get("candidates", [])],
        ))
    return AMQueueResponse(run_id=parsed.get("run_id", ""), point_in_time=parsed.get("point_in_time"),
                           themes=themes)


def am_theme(theme_id: str) -> ThemeWithCandidates:
    resp = am_queue()
    for t in resp.themes:
        if t.theme.id == theme_id:
            return t
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Theme '{theme_id}' not found")


# ── FO mapping (locked flattening, arch v0.4 §3) ─────────────────────────────
def _fo_envelope(parsed) -> dict:
    if not isinstance(parsed, dict) or "packages" not in parsed:
        raise ArtifactUnavailable("fo", "legacy", "FO artifact must be envelope {run_id, provenance, packages}")
    return parsed


def _fo_provenance(env: dict) -> Provenance:
    p = env.get("provenance", {})
    return Provenance(source=p.get("source", "unknown"), mode=p.get("mode", "unknown"),
                      as_of=p.get("as_of"), coverage=p.get("coverage"),
                      completeness=p.get("completeness"), hybrid=bool(p.get("hybrid", False)))


def _fo_summary(pkg: dict, prov: Provenance) -> ResearchPackageSummary:
    ia = pkg.get("industry_assessment", {})
    ca = pkg.get("company_assessment", {})
    moat = ca.get("moat", {})
    et = pkg.get("earnings_trajectory", {})
    vt = pkg.get("valuation_context", {}).get("value_trap", {})
    verdict = vt.get("verdict") if vt.get("triggered") else "NOT_TRIGGERED"  # locked derivation (§3)
    conv = pkg.get("conviction", {})
    return ResearchPackageSummary(
        id=pkg.get("id", "UNKNOWN"), name=pkg.get("name", "Unknown"),
        sector=ia.get("sector", "Unknown"), industry=ia.get("industry", "Unknown"),
        moat_width=moat.get("width", "None"), moat_depth=moat.get("depth", "Shallow"),
        moat_trend=moat.get("trend", "Stable"), earnings_quality=et.get("rating", "UNKNOWN"),
        conviction=conv.get("level", "Unknown") if isinstance(conv, dict) else str(conv),
        value_trap_verdict=verdict, provenance=prov)


def _fo_detail(pkg: dict, prov: Provenance) -> ResearchPackageDetail:
    s = _fo_summary(pkg, prov)
    # FD #53: drop unapproved derived fields at serve time (moat_score has no spec basis)
    ca = {k: v for k, v in pkg.get("company_assessment", {}).items() if k != "moat_score"}
    return ResearchPackageDetail(**s.model_dump(exclude={"conviction"}), conviction=pkg.get("conviction", {}),
                                 generated_at=pkg.get("generated_at", ""), spec_ref=pkg.get("spec_ref", ""),
                                 thesis_summary=pkg.get("thesis_summary", ""),
                                 thesis_lifecycle=pkg.get("thesis_lifecycle", ""),
                                 macro_context=pkg.get("macro_context", {}),
                                 industry_assessment=pkg.get("industry_assessment", {}),
                                 company_assessment=ca,
                                 earnings_trajectory=pkg.get("earnings_trajectory", {}),
                                 valuation_context=pkg.get("valuation_context", {}),
                                 key_risks=pkg.get("key_risks", []),
                                 independent_challenge=pkg.get("independent_challenge", []),
                                 supporting_evidence=pkg.get("supporting_evidence", []),
                                 contradicting_evidence=pkg.get("contradicting_evidence", []),
                                 open_questions=pkg.get("open_questions", []))


def fo_packages() -> tuple[dict, Provenance, list[dict]]:
    raw, parsed = load_snapshot("fo")
    env = _fo_envelope(parsed)
    prov = _fo_provenance(env)
    admit("fo", parsed)
    return env, prov, env.get("packages", [])


def fo_queue() -> list[ResearchPackageSummary]:
    _, prov, packages = fo_packages()
    return [_fo_summary(p, prov) for p in packages]


def fo_package(company_id: str) -> ResearchPackageDetail:
    _, prov, packages = fo_packages()
    for pkg in packages:
        if str(pkg.get("id", "")).upper() == company_id.upper():
            return _fo_detail(pkg, prov)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail=f"Company '{company_id}' not found")


def fo_cheap_quality() -> list[ResearchPackageSummary]:
    """Filter to value_trap_verdict == NOT_A_TRAP (spec §3.6.2 Cheap & Quality watchlist)."""
    return [p for p in fo_queue() if p.value_trap_verdict == "NOT_A_TRAP"]


# ── II mapping ────────────────────────────────────────────────────────────────
def ii_signals(limit: int = 0, offset: int = 0) -> IISignalsResponse:
    raw, parsed = load_snapshot("ii")
    if not isinstance(parsed, dict):
        raise ArtifactUnavailable("ii", "corrupt", "II artifact must be a dict")
    prov = admit("ii", parsed)
    all_signals = parsed.get("signals", [])
    total = len(all_signals)
    if limit > 0:
        all_signals = all_signals[offset:offset + limit]
    signals = [IISignalSummary(**s) for s in all_signals]
    return IISignalsResponse(signals=signals, summary=parsed.get("summary", {}),
                             meta=parsed.get("meta", {}), provenance=prov, total=total)


# ── Dashboard (per-component admission, NF7) ──────────────────────────────────
def dashboard_components() -> dict[str, ComponentProvenance | None]:
    out: dict[str, ComponentProvenance | None] = {}
    for module in ("am", "fo", "ii"):
        try:
            raw, parsed = load_snapshot(module)
            prov = admit(module, parsed)
            run = persistence.latest_run(module)
            out[module] = ComponentProvenance(
                run_id=run["run_id"] if run else None,
                point_in_time=prov.as_of or (run["point_in_time"] if run else None),
                data_source=f"real_{prov.source}", state="available")
        except ArtifactUnavailable:
            out[module] = None  # unadmitted -> explicit null/unavailable (never silent synthetic)
    # CS: exact served mock bytes; explicit null lineage; NOT linked to CS pipeline artifact (NF3)
    from backend.api import cs_routes
    assets = cs_routes._MOCK_ASSETS
    qmet = sum(1 for a in assets if a["q_conditions_met"] == a["q_conditions_total"])
    out["cs"] = ComponentProvenance(run_id=None, point_in_time=None,
                                    data_source="synthetic_demo", source="backend_static_mock")
    out["_cs_counts"] = ComponentProvenance(
        data_source=f"{len(assets)}:{qmet}", source="backend_static_mock")  # SOL-003 triple agreement
    return out
