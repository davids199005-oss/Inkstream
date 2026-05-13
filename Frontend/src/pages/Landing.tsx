import { useNavigate } from 'react-router'

export default function Landing() {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col min-h-dvh bg-[#FAFAF7]">
      <header className="px-8 py-6">
        <span className="font-mono text-sm font-semibold text-[#0A0A0A] tracking-tight">Inkstream</span>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-8 text-center">
        <h1 className="font-mono text-5xl font-semibold text-[#0A0A0A] tracking-tighter mb-4">
          Inkstream
        </h1>
        <p className="text-[#888] text-base mb-10 max-w-sm">
          Words flowing from the model.
        </p>
        <button
          onClick={() => navigate('/home')}
          className="inline-flex items-center gap-2 bg-[#E85D2C] text-white text-sm font-medium px-6 py-3 rounded-full hover:bg-[#d04f22] transition-colors cursor-pointer"
        >
          Start chatting
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2 7H12M12 7L7 2M12 7L7 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </main>

      <footer className="px-8 py-6 text-center">
        <p className="text-xs text-[#CCC] font-mono">© 2026 Inkstream</p>
      </footer>
    </div>
  )
}
