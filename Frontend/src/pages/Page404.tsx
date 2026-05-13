import { useNavigate } from 'react-router'

export default function Page404() {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col min-h-dvh bg-[#FAFAF7] items-center justify-center px-8 text-center">
      <p className="font-mono text-6xl font-semibold text-[#E8E8E4] mb-4">404</p>
      <p className="text-sm text-[#888] mb-8">This page doesn't exist.</p>
      <button
        onClick={() => navigate('/')}
        className="text-sm text-[#E85D2C] hover:underline cursor-pointer"
      >
        ← Back to home
      </button>
    </div>
  )
}
