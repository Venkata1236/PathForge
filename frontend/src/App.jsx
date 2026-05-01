import { Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from './components/ui/Toaster.jsx'
import OnboardingPage from './pages/OnboardingPage.jsx'
import PathPage from './pages/PathPage.jsx'
import HistoryPage from './pages/HistoryPage.jsx'

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<OnboardingPage />} />
        <Route path="/path" element={<PathPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <Toaster />
    </>
  )
}

export default App