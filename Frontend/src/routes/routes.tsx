import { BrowserRouter, Routes, Route } from 'react-router'
import Home from '../pages/Home'
import About from '../pages/About'
import Page404 from '../pages/Page404'

export default function Navigation() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<Page404 />} />
      </Routes>
    </BrowserRouter>
  )
}