import { useState, useEffect, useCallback, useRef } from 'react'
import { api } from '../lib/api'
import type { Message } from '../types'

interface UseChatReturn {
  messages: Message[]
  assistantDraft: string
  isStreaming: boolean
  error: string | null
  sendMessage: (content: string) => Promise<void>
  abortStream: () => void
}

export function useChat(
  conversationId: string | null,
  onTitleUpdate?: (id: string, title: string) => void
): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([])
  const [assistantDraft, setAssistantDraft] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const abortRef = useRef<AbortController | null>(null)
  const tokenBufferRef = useRef('')

  useEffect(() => {
    abortRef.current?.abort()
    setMessages([])
    setAssistantDraft('')
    tokenBufferRef.current = ''
    setIsStreaming(false)
    setError(null)

    if (!conversationId) return

    const load = async () => {
      try {
        const detail = await api.getConversation(conversationId)
        setMessages(detail.messages)
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Failed to load messages')
      }
    }
    load()
  }, [conversationId])

  const sendMessage = useCallback(async (content: string) => {
    if (!conversationId || isStreaming) return

    setIsStreaming(true)
    setError(null)
    tokenBufferRef.current = ''

    const controller = new AbortController()
    abortRef.current = controller

    try {
      await api.streamMessage(
        conversationId,
        content,
        {
          onUserMessage: (msg) => setMessages(prev => [...prev, msg]),
          onToken: (text) => {
            tokenBufferRef.current += text
            setAssistantDraft(prev => prev + text)
          },
          onDone: (messageId, title) => {
            const finalContent = tokenBufferRef.current
            tokenBufferRef.current = ''
            setMessages(prev => [
              ...prev,
              {
                id: messageId,
                conversation_id: conversationId,
                role: 'assistant',
                content: finalContent,
                created_at: new Date().toISOString(),
              },
            ])
            setAssistantDraft('')
            setIsStreaming(false)
            if (title) onTitleUpdate?.(conversationId, title)
          },
          onError: (message) => {
            tokenBufferRef.current = ''
            setAssistantDraft('')
            setIsStreaming(false)
            setError(message)
          },
        },
        controller.signal
      )
    } catch (e) {
      tokenBufferRef.current = ''
      setAssistantDraft('')
      setIsStreaming(false)
      if (e instanceof Error && e.name !== 'AbortError') {
        setError(e.message)
      }
    }
  }, [conversationId, isStreaming, onTitleUpdate])

  const abortStream = useCallback(() => {
    abortRef.current?.abort()
    tokenBufferRef.current = ''
    setAssistantDraft('')
    setIsStreaming(false)
  }, [])

  return { messages, assistantDraft, isStreaming, error, sendMessage, abortStream }
}
