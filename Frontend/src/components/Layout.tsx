import { Outlet } from 'react-router'
import Navbar from './Navbar'

export default function Layout() {
  return (
    <div className="flex flex-col h-dvh bg-[#FAFAF7]">
      <Navbar />
      <main className="flex-1 min-h-0">
        <Outlet />
      </main>
    </div>
  )
}
