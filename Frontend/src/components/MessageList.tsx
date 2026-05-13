import { useEffect, useRef } from 'react'
import type { Message } from '../types'
import MessageItem from './MessageItem'

interface Props {
  messages: Message[]
  assistantDraft: string
  isStreaming: boolean
}

export default function MessageList({ messages, assistantDraft, isStreaming }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, assistantDraft])

  if (messages.length === 0 && !isStreaming) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <p className="text-sm text-[#AAA] font-mono">Start a conversation...</p>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto py-6 space-y-2">
      {messages.map(msg => (
        <MessageItem key={msg.id} role={msg.role} content={msg.content} />
      ))}
      {isStreaming && assistantDraft && (
        <MessageItem role="assistant" content={assistantDraft} isStreaming />
      )}
      <div ref={bottomRef} />
    </div>
  )
}
