import { BrowserRouter, Routes, Route } from 'react-router'
import Home from '../pages/Home'
import About from '../pages/About'
import Page404 from '../pages/Page404'
import Landing from '../pages/Landing'
import Layout from '../components/Layout'

export default function Navigation() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route element={<Layout />}>
        <Route path="/home" element={<Home />} />
        <Route path="/about" element={<About />} />
        </Route>
        <Route path="*" element={<Page404 />} />
      </Routes>
    </BrowserRouter>
  )
}