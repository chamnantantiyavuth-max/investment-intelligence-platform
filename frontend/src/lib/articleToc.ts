/**
 * Article TOC helper — extract h2 headings from the rendered article body
 * into a stable {id, text} list for the table of contents (PLAN
 * ARTICLE-READABILITY v0.1, Option A, 10 Aug 2026).
 *
 * Pure function — no DOM access here; callers pass the article element.
 */

export interface TocEntry {
  /** URL-safe anchor id, also assigned to the h2 element. */
  id: string;
  /** Heading text with leading section numbers stripped ("1. Business model" → "Business model"). */
  text: string;
  /** Original heading text (numbered form kept for display in the TOC). */
  raw: string;
}

export function slugifyHeading(text: string): string {
  return text
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9\u0e00-\u0e7f]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

/** Strip leading section numbers: "1. Business model" → "Business model", "01" → "01" untouched. */
export function stripSectionNumber(text: string): string {
  return text.replace(/^\s*\d+\.\s+/, "").trim();
}

export function extractToc(root: ParentNode): TocEntry[] {
  const out: TocEntry[] = [];
  const seen = new Map<string, number>();
  root.querySelectorAll("h2").forEach((h) => {
    const raw = h.textContent?.trim() ?? "";
    if (!raw) return;
    const text = stripSectionNumber(raw);
    let id = slugifyHeading(text) || "section";
    const n = seen.get(id) ?? 0;
    seen.set(id, n + 1);
    if (n > 0) id = `${id}-${n}`;
    h.id = id;
    // Headings already numbered in the source markdown ("1. Business model")
    // keep their own numeral — suppress the CSS ghost numeral to avoid dupes.
    if (/^\d+\.\s/.test(raw)) h.classList.add("has-number");
    out.push({ id, text, raw });
  });
  return out;
}
