/**
 * Article table of contents — auto-generated from the article's h2 sections.
 * Magazine treatment (PLAN ARTICLE-READABILITY v0.1, Option A):
 * small-caps mono numerals + hairline separators, no boxes (FD-032).
 * Desktop: sticky rail under the title. Mobile: collapsible <details>.
 * Scrollspy via IntersectionObserver — current section highlighted.
 */
import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";
import type { TocEntry } from "@/lib/articleToc";

export function ArticleToc({ entries }: { entries: TocEntry[] }) {
  const [active, setActive] = useState<string | null>(entries[0]?.id ?? null);
  const [open, setOpen] = useState(false);
  const observer = useRef<IntersectionObserver | null>(null);

  useEffect(() => {
    if (!entries.length) return;
    const ids = entries.map((e) => e.id);
    observer.current = new IntersectionObserver(
      (sections) => {
        for (const s of sections) {
          if (s.isIntersecting) setActive(s.target.id);
        }
      },
      { rootMargin: "-15% 0px -70% 0px", threshold: 0 }
    );
    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.current?.observe(el);
    });
    return () => observer.current?.disconnect();
  }, [entries]);

  if (!entries.length) return null;

  const list = (
    <nav aria-label="Sections" className="border-t-2 border-ink pt-3">
      <ul className="space-y-1.5">
        {entries.map((e, i) => (
          <li key={e.id}>
            <a
              href={`#${e.id}`}
              onClick={() => setOpen(false)}
              className={cn(
                "group flex items-baseline gap-3 text-[12.5px] leading-snug transition-colors",
                active === e.id ? "text-primary" : "text-ink-2 hover:text-foreground"
              )}
            >
              <span className="w-6 shrink-0 font-mono text-[10px] tabular-nums text-ink-3 group-hover:text-primary">
                {String(i + 1).padStart(2, "0")}
              </span>
              <span>{e.text}</span>
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );

  return (
    <div className="mt-8">
      {/* Desktop: inline block below title (no sticky rail — keeps 65ch measure clean) */}
      <div className="hidden md:block">{list}</div>
      {/* Mobile: collapsible */}
      <details className="md:hidden" open={open} onToggle={(ev) => setOpen((ev.target as HTMLDetailsElement).open)}>
        <summary className="cursor-pointer list-none text-[11px] font-bold uppercase tracking-[0.12em] text-primary">
          Sections
        </summary>
        <div className="mt-2">{list}</div>
      </details>
    </div>
  );
}
