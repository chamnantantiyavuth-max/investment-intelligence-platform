import type { OrgCard } from "@/api/orgClient";

/** Review gate statuses — text rows, never a linear progress bar
 *  (some gates run in parallel; a bar would imply a single sequence). */
export function ReviewGatePanel({ card }: { card: OrgCard }) {
  const rows: Array<[string, string]> = [
    ["Data", card.data_status],
    ["Validation", card.validation_status],
    ["Risk", card.risk_status],
    ["Audit", card.audit_status || "NOT ASSESSED"],
    ["Artifact", card.artifact_state ?? "—"],
    ["Approval", card.approval_status ?? "no canonical state"],
  ];
  return (
    <div className="grid gap-x-8 gap-y-1 text-[13px] sm:grid-cols-2">
      {rows.map(([k, v]) => (
        <div key={k} className="flex justify-between border-b border-rule py-1.5">
          <span className="text-ink-2">{k}</span>
          <span className="font-mono text-[11px] text-ink-3">{v}</span>
        </div>
      ))}
    </div>
  );
}
