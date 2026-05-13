import type { Conversation, Message } from './models'

export interface SidebarProps {
  conversations: Conversation[]
  activeId: string | null
  onSelect: (id: string) => void
  onCreate: () => void
  onDelete: (id: string) => void
}

export interface MessageItemProps {
  role: 'user' | 'assistant'
  content: string
  isStreaming?: boolean
}

export interface MessageListProps {
  messages: Message[]
  assistantDraft: string
  isStreaming: boolean
}

export interface ChatInputProps {
  onSend: (content: string) => void
  isStreaming: boolean
  disabled?: boolean
}
