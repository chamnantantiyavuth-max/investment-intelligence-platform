import { Outlet } from "react-router-dom"
import { Masthead } from "@/components/Masthead"
import { AdvisoryFooter } from "@/components/AdvisoryFooter"

/** Research Desk shell — masthead top bar, single content column (IA: no left rail). */
export function Layout() {
  return (
    <div className="flex min-h-screen flex-col">
      <Masthead />
      <main className="mx-auto w-full max-w-[1200px] flex-1 px-6 py-6">
        <Outlet />
      </main>
      <AdvisoryFooter />
    </div>
  )
}
