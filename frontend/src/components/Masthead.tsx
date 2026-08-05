import { NavLink } from "react-router-dom"

const NAV = [
  { to: "/", label: "Briefing", end: true },
  { to: "/research", label: "Research Desk" },
  { to: "/am-queue", label: "Alpha Momentum" },
  { to: "/cs-radar", label: "Close System" },
  { to: "/fundamental", label: "Fundamental" },
  { to: "/institutional", label: "Institutional" },
  { to: "/weak-signals", label: "Weak Signals" },
]

/** Research Desk masthead — newspaper-of-record brand + small-caps nav + run stamp. */
export function Masthead() {
  return (
    <header className="masthead sticky top-0 z-40 bg-background">
      <div className="mx-auto flex max-w-[1200px] items-baseline gap-6 px-6 py-3">
        <div className="font-display text-lg font-bold tracking-tight">
          Investment Intelligence <span className="text-primary">Platform</span>
        </div>
        <nav className="flex flex-wrap items-baseline gap-4 text-[11px] font-semibold uppercase tracking-[0.12em]">
          {NAV.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.end}
              className={({ isActive }) =>
                isActive ? "border-b-2 border-primary pb-0.5 text-foreground" : "pb-0.5 text-ink-2 hover:text-foreground"
              }
            >
              {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="ml-auto hidden font-mono text-[11px] text-ink-3 md:block" data-testid="run-stamp">
          advisory · portfolio-blind
        </div>
      </div>
    </header>
  )
}
