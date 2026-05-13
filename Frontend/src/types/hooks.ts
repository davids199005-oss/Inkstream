import type { Conversation, Message } from './models'

export interface UseConversationsReturn {
  conversations: Conversation[]
  activeId: string | null
  loading: boolean
  error: string | null
  fetchAll: () => Promise<Conversation[]>
  create: () => Promise<void>
  remove: (id: string) => Promise<void>
  setActive: (id: string | null) => void
  updateTitle: (id: string, title: string) => void
}

export interface UseChatReturn {
  messages: Message[]
  assistantDraft: string
  isStreaming: boolean
  error: string | null
  sendMessage: (content: string) => Promise<void>
  abortStream: () => void
}
