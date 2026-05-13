export default function About() {
  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-2xl mx-auto px-8 py-12">
        <h1 className="font-mono text-2xl font-semibold text-[#0A0A0A] tracking-tight mb-2">
          About Inkstream
        </h1>
        <p className="text-[#888] text-sm font-mono mb-10">Words flowing from the model.</p>

        <section className="mb-8">
          <p className="text-sm text-[#0A0A0A] leading-relaxed">
            Inkstream is a conversational AI interface built on top of OpenAI's GPT-4o-mini model.
            It features real-time streaming responses, automatic conversation title generation,
            and a clean, minimal design.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-xs font-semibold text-[#888] uppercase tracking-widest mb-3">Tech Stack</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs font-semibold text-[#0A0A0A] mb-1.5">Backend</p>
              <ul className="space-y-1">
                {['Python 3.14', 'FastAPI', 'MongoDB', 'OpenAI SDK', 'SSE Streaming'].map(item => (
                  <li key={item} className="text-sm text-[#555] flex items-center gap-2">
                    <span className="w-1 h-1 rounded-full bg-[#E85D2C] shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="text-xs font-semibold text-[#0A0A0A] mb-1.5">Frontend</p>
              <ul className="space-y-1">
                {['React 19', 'TypeScript', 'Tailwind CSS v4', 'Vite 8', 'React Router v7'].map(item => (
                  <li key={item} className="text-sm text-[#555] flex items-center gap-2">
                    <span className="w-1 h-1 rounded-full bg-[#E85D2C] shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        <section className="mb-10">
          <h2 className="text-xs font-semibold text-[#888] uppercase tracking-widest mb-3">Author</h2>
          <p className="text-sm text-[#0A0A0A]">David Veryutin</p>
          <p className="text-xs text-[#888] mt-0.5">Final project · John Bryce Full Stack & GenAI · 2026</p>
        </section>

        <footer className="pt-8 border-t border-[#E8E8E4]">
          <p className="text-xs text-[#CCC] font-mono">© 2026 Inkstream</p>
        </footer>
      </div>
    </div>
  )
}
