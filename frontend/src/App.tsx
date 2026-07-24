import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Layout } from "@/components/Layout"
import DashboardPage from "@/pages/DashboardPage"
import AMQueuePage from "@/pages/AMQueuePage"
import AMThemeCardPage from "@/pages/AMThemeCardPage"
import CSRadarPage from "@/pages/CSRadarPage"
import WeakSignalInboxPage from "@/pages/WeakSignalInboxPage"
import NotFoundPage from "@/pages/NotFoundPage"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="am-queue" element={<AMQueuePage />} />
          <Route path="am-theme/:id" element={<AMThemeCardPage />} />
          <Route path="cs-radar" element={<CSRadarPage />} />
          <Route path="weak-signals" element={<WeakSignalInboxPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
