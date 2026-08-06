import { useEffect, useState } from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Layout } from "@/components/Layout"
import { authStatus } from "@/api/authClient"
import LoginPage from "@/pages/LoginPage"
import DashboardPage from "@/pages/DashboardPage"
import ResearchDeskPage from "@/pages/ResearchDeskPage"
import KanbanBoardPage from "@/pages/KanbanBoardPage"
import ResearchArtifactDetailPage from "@/pages/ResearchArtifactDetailPage"
import AMQueuePage from "@/pages/AMQueuePage"
import AMScreenerPage from "@/pages/AMScreenerPage"
import AMThemeCardPage from "@/pages/AMThemeCardPage"
import CSRadarPage from "@/pages/CSRadarPage"
import CSProductDetailPage from "@/pages/CSProductDetailPage"
import FundamentalQueuePage from "@/pages/FundamentalQueuePage"
import FundamentalDetailPage from "@/pages/FundamentalDetailPage"
import CheapQualityPage from "@/pages/CheapQualityPage"
import InstitutionalPage from "@/pages/InstitutionalPage"
import WeakSignalInboxPage from "@/pages/WeakSignalInboxPage"
import NotFoundPage from "@/pages/NotFoundPage"

function AuthGate({ children }: { children: React.ReactNode }) {
  const [authed, setAuthed] = useState<boolean | null>(null)

  useEffect(() => {
    authStatus().then(setAuthed)
  }, [])

  if (authed === null) {
    return <div className="flex min-h-screen items-center justify-center text-sm text-slate-500">Loading…</div>
  }
  if (!authed) {
    return <LoginPage onSuccess={() => setAuthed(true)} />
  }
  return <>{children}</>
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthGate>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<DashboardPage />} />
            <Route path="research" element={<ResearchDeskPage />} />
            <Route path="kanban" element={<KanbanBoardPage />} />
            <Route path="research/*" element={<ResearchArtifactDetailPage />} />
            <Route path="am-queue" element={<AMQueuePage />} />
            <Route path="am-screener" element={<AMScreenerPage />} />
            <Route path="am-theme/:id" element={<AMThemeCardPage />} />
            <Route path="cs-radar" element={<CSRadarPage />} />
            <Route path="cs-radar/:id" element={<CSProductDetailPage />} />
            <Route path="fundamental" element={<FundamentalQueuePage />} />
            <Route path="fundamental/:id" element={<FundamentalDetailPage />} />
            <Route path="cheap-quality" element={<CheapQualityPage />} />
            <Route path="institutional" element={<InstitutionalPage />} />
            <Route path="weak-signals" element={<WeakSignalInboxPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </AuthGate>
    </BrowserRouter>
  )
}
