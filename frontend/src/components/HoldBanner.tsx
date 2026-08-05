import type { OrgHold } from "@/api/orgClient";

/** Full hold banner — a Hold is never a small badge (fit-gap component verdict).
 *  Active holds render expanded; cleared holds render a collapsed one-liner. */
export function HoldBanner({ hold, active = true }: { hold: OrgHold; active?: boolean }) {
  if (!active) {
    return (
      <div className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5 py-1 text-[11px] text-ink-2">
        <span className="font-mono uppercase tracking-[0.1em] text-ink-3">{hold.type}</span>
        <span>{hold.hold_id}</span>
        <span>cleared {hold.clear_record?.date ?? ""}</span>
        <span>by {hold.clear_record?.cleared_by ?? hold.issuer}</span>
      </div>
    );
  }
  return (
    <div className="rounded-md bg-bg-panel px-4 py-3" role="status">
      <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-warning">
        {hold.type} · {hold.hold_id}
      </p>
      <p className="mt-1 text-sm text-foreground">
        Issued by: <span className="font-medium">{hold.issuer}</span>
      </p>
      <p className="mt-0.5 text-xs text-ink-2">Reason: {hold.triggering_condition || hold.evidence}</p>
      <p className="mt-0.5 text-xs text-ink-2">Affected output: {hold.artifact}</p>
      {hold.remediation_required && (
        <p className="mt-0.5 text-xs text-ink-2">
          Clearance requires: <span className="text-foreground">{hold.remediation_required}</span>
        </p>
      )}
      <p className="mt-1 text-[11px] text-ink-3">
        owner {hold.owner} · review: {hold.review_condition}
      </p>
    </div>
  );
}
