import { Link } from "react-router-dom";
import type { ResearchArtifact } from "@/api/orgClient";

/** Immutable decision timeline — every entry is a recorded event (artifact
 *  modification, status, Founder publication transition from the founder
 *  review record's own transition table). Corrections render as replacements
 *  (append-first, PUBLICATION-STANDARD), never edits to prior entries. */
function clean(s: string, max = 90): string {
  return s.replace(/\*\*/g, "").replace(/`/g, "").split(/\s*;\s*/)[0].trim().slice(0, max);
}

interface Transition {
  prior?: string;
  next?: string;
  actor?: string;
  timestamp?: string;
}

/** Parse the founder-review-record "Publication Transition" table rows. */
const KEY_MAP: Record<string, keyof Transition> = {
  "Prior state": "prior",
  "New state": "next",
  Actor: "actor",
  Timestamp: "timestamp",
};

function parseTransition(content?: string): Transition {
  const t: Transition = {};
  if (!content) return t;
  for (const line of content.split(/\r?\n/)) {
    const m = line.match(/^\|\s*(Prior state|New state|Actor|Timestamp)\s*\|\s*(.+?)\s*\|/);
    if (m) {
      const key = KEY_MAP[m[1]];
      t[key] = m[2].replace(/\*\*/g, "").replace(/`/g, "").trim();
    }
  }
  return t;
}

export interface FounderRecord {
  artifact: ResearchArtifact;
  content?: string;
}

export function DecisionTimeline({
  artifact,
  records,
}: {
  artifact: ResearchArtifact;
  records: FounderRecord[];
}) {
  const events: Array<[string, string, React.ReactNode, string | undefined]> = [];
  if (artifact.modified) events.push([artifact.modified, "artifact", "modified", undefined]);
  if (artifact.research_status) events.push(["—", "status", clean(artifact.research_status), undefined]);
  for (const r of records) {
    const t = parseTransition(r.content);
    const label = t.prior && t.next ? `${t.prior} → ${t.next}` : r.artifact.title;
    events.push([
      t.timestamp || r.artifact.modified,
      "founder decision",
      label,
      r.artifact.artifact_id,
    ]);
  }
  if (events.length === 0) {
    return <p className="text-xs text-ink-2">No recorded decision events for this artifact yet.</p>;
  }
  return (
    <div className="space-y-1">
      {events.map(([date, kind, text, link], i) => (
        <div key={i} className="flex items-baseline gap-3 border-b border-rule py-1.5 text-[13px]">
          <span className="w-24 shrink-0 font-mono text-[11px] text-ink-3">{date}</span>
          <span className="w-32 shrink-0 text-[11px] uppercase tracking-[0.08em] text-ink-3">{kind}</span>
          {link ? (
            <Link to={`/research/${link}`} className="text-primary hover:underline">
              {text}
            </Link>
          ) : (
            <span className="text-foreground">{text}</span>
          )}
        </div>
      ))}
    </div>
  );
}
