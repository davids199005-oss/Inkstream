import type { SidebarProps } from '../types/components'

export default function Sidebar({ conversations, activeId, onSelect, onCreate, onDelete }: SidebarProps) {
  return (
    <aside className="flex flex-col w-64 shrink-0 h-full border-r border-[#E8E8E4] bg-[#F3F3EF]">
      <div className="p-3 border-b border-[#E8E8E4]">
        <button
          onClick={onCreate}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-[#0A0A0A] hover:bg-[#E8E8E4] transition-colors cursor-pointer"
        >
          <span className="text-lg leading-none">+</span>
          New chat
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto p-2 space-y-0.5">
        {conversations.length === 0 && (
          <p className="px-3 py-4 text-xs text-[#888] text-center">No conversations yet</p>
        )}
        {conversations.map(conv => (
          <div
            key={conv.id}
            className={`group flex items-center gap-1 rounded-lg px-3 py-2 cursor-pointer transition-colors ${
              conv.id === activeId
                ? 'bg-[#E85D2C] text-white'
                : 'text-[#0A0A0A] hover:bg-[#E8E8E4]'
            }`}
            onClick={() => onSelect(conv.id)}
          >
            <span className="flex-1 text-sm truncate">{conv.title}</span>
            <button
              onClick={e => { e.stopPropagation(); onDelete(conv.id) }}
              className={`shrink-0 opacity-0 group-hover:opacity-100 transition-opacity text-xs px-1 rounded hover:bg-black/10 cursor-pointer ${
                conv.id === activeId ? 'text-white/80' : 'text-[#888]'
              }`}
              aria-label="Delete conversation"
            >
              ✕
            </button>
          </div>
        ))}
      </nav>
    </aside>
  )
}
