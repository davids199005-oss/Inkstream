import { NavLink } from 'react-router'

export default function Navbar() {
  return (
    <header className="shrink-0 flex items-center justify-between px-4 h-12 border-b border-[#E8E8E4] bg-[#FAFAF7]">
      <NavLink to="/" className="font-mono text-sm font-semibold text-[#0A0A0A] tracking-tight">
        Inkstream
      </NavLink>
      <nav className="flex items-center gap-4">
        <NavLink
          to="/home"
          className={({ isActive }) =>
            `text-sm transition-colors ${isActive ? 'text-[#E85D2C] font-medium' : 'text-[#888] hover:text-[#0A0A0A]'}`
          }
        >
          Chat
        </NavLink>
        <NavLink
          to="/about"
          className={({ isActive }) =>
            `text-sm transition-colors ${isActive ? 'text-[#E85D2C] font-medium' : 'text-[#888] hover:text-[#0A0A0A]'}`
          }
        >
          About
        </NavLink>
      </nav>
    </header>
  )
}
