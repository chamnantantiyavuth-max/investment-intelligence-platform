// SyntheticDataBanner — unmissable provenance label for demo/synthetic surfaces.
// Truth-safety per Constitution §§8/10/11/23.4 and DNA-002/DNA-016:
// any page showing values that are NOT live pipeline output must carry this banner.
import { FlaskConical } from "lucide-react";

export default function SyntheticDataBanner({
  note = "Demonstration data — not live market output. Informational only; not investment advice.",
}: {
  note?: string;
}) {
  return (
    <div className="flex items-start gap-2 rounded-lg border border-amber-300 bg-amber-50 px-3 py-2">
      <FlaskConical className="mt-0.5 size-4 shrink-0 text-amber-600" />
      <div className="text-xs text-amber-800">
        <span className="font-bold uppercase tracking-wide">Synthetic demo data — not live market data</span>
        <span className="block mt-0.5">{note}</span>
      </div>
    </div>
  );
}
