import { useState, useCallback } from 'react'
import { api } from '../lib/api'
import type { Conversation } from '../types/models'
import type { UseConversationsReturn } from '../types/hooks'

export function useConversations(): UseConversationsReturn {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchAll = useCallback(async (): Promise<Conversation[]> => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.getConversations()
      setConversations(data)
      return data
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load conversations')
      return []
    } finally {
      setLoading(false)
    }
  }, [])

  const create = useCallback(async () => {
    setError(null)
    try {
      const newConv = await api.createConversation()
      setConversations(prev => [newConv, ...prev])
      setActiveId(newConv.id)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to create conversation')
    }
  }, [])

  const remove = useCallback(async (id: string) => {
    setError(null)
    try {
      await api.deleteConversation(id)
      setConversations(prev => {
        const updated = prev.filter(c => c.id !== id)
        setActiveId(current =>
          current === id ? (updated[0]?.id ?? null) : current
        )
        return updated
      })
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to delete conversation')
    }
  }, [])

  const updateTitle = useCallback((id: string, title: string) => {
    setConversations(prev =>
      prev.map(c => c.id === id ? { ...c, title } : c)
    )
  }, [])

  return {
    conversations,
    activeId,
    loading,
    error,
    fetchAll,
    create,
    remove,
    setActive: setActiveId,
    updateTitle,
  }
}
