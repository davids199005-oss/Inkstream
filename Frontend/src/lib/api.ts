import type { Conversation, ConversationDetail } from '../types/models'
import type { StreamCallbacks } from '../types/api'
import { AppConfig } from '../config/AppConfig'

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail ?? `HTTP ${res.status}`)
  }

  if (res.status === 204) return undefined as T
  return res.json()
}

export const api = {
  getConversations: (): Promise<Conversation[]> =>
    request(AppConfig.CONVERSATIONS_PATH),

  createConversation: (): Promise<Conversation> =>
    request(AppConfig.CONVERSATIONS_PATH, { method: 'POST', body: JSON.stringify({}) }),

  getConversation: (id: string): Promise<ConversationDetail> =>
    request(AppConfig.CONVERSATION_PATH.replace(':id', id)),

  deleteConversation: (id: string): Promise<void> =>
    request(AppConfig.CONVERSATION_PATH.replace(':id', id), { method: 'DELETE' }),

  streamMessage: async (
    conversationId: string,
    content: string,
    callbacks: StreamCallbacks,
    signal?: AbortSignal
  ): Promise<void> => {
    const url = AppConfig.MESSAGES_PATH.replace(':id', conversationId)
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content }),
      signal,
    })

    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(error.detail ?? `HTTP ${res.status}`)
    }

    const reader = res.body!.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let currentEvent = ''
    let currentData = ''

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        if (signal?.aborted) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''

        for (const line of lines) {
          if (line.startsWith('event:')) {
            currentEvent = line.slice(6).trim()
          } else if (line.startsWith('data:')) {
            currentData = line.slice(5).trim()
          } else if (line === '') {
            if (currentEvent && currentData) {
              try {
                const parsed = JSON.parse(currentData)
                switch (currentEvent) {
                  case 'user_message_saved':
                    callbacks.onUserMessage(parsed)
                    break
                  case 'token':
                    callbacks.onToken(parsed.text)
                    break
                  case 'done':
                    callbacks.onDone(parsed.message_id, parsed.title ?? null)
                    break
                  case 'error':
                    callbacks.onError(parsed.message)
                    break
                }
              } catch {
                // malformed JSON — skip
              }
            }
            currentEvent = ''
            currentData = ''
          }
        }
      }
    } finally {
      reader.releaseLock()
    }
  },
}
