import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import SearchPage from './pages/SearchPage'
import ServerPage from './pages/ServerPage'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/server/:id" element={<ServerPage />} />
      </Routes>
    </Layout>
  )
}
