import { useEffect, useState } from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { Layout } from "@/components/Layout"
import { authStatus } from "@/api/authClient"
import LoginPage from "@/pages/LoginPage"
import KanbanBoardPage from "@/pages/KanbanBoardPage"
import OrgOfficePage from "@/pages/OrgOfficePage"
import LibraryPage from "@/pages/LibraryPage"
import ReportArticlePage from "@/pages/ReportArticlePage"
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
          {/* Research blog — primary surface, standalone magazine shell (FD #84; FD #86: `/` → blog). */}
          <Route path="/" element={<Navigate to="/library" replace />} />
          <Route path="library" element={<LibraryPage />} />
          <Route path="library/:slug" element={<ReportArticlePage />} />

          {/* Old platform — trimmed to Org Office + Kanban Board only (FD #86; routes deleted). */}
          <Route element={<Layout />}>
            <Route path="kanban" element={<KanbanBoardPage />} />
            <Route path="org-office" element={<OrgOfficePage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </AuthGate>
    </BrowserRouter>
  )
}
