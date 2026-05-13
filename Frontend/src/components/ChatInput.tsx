import { useState, useRef, useEffect } from 'react'
import type { ChatInputProps } from '../types'

export default function ChatInput({ onSend, isStreaming, disabled }: ChatInputProps) {
  const [value, setValue] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (!isStreaming && textareaRef.current) {
      textareaRef.current.focus()
    }
  }, [isStreaming])

  const handleSubmit = () => {
    const trimmed = value.trim()
    if (!trimmed || isStreaming || disabled) return
    onSend(trimmed)
    setValue('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleInput = () => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`
  }

  const canSend = value.trim().length > 0 && !isStreaming && !disabled

  return (
    <div className="shrink-0 border-t border-[#E8E8E4] bg-[#FAFAF7] px-4 py-3">
      <div className="flex items-end gap-2 max-w-3xl mx-auto">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          placeholder={isStreaming ? 'Waiting for response...' : 'Message Inkstream...'}
          disabled={isStreaming || disabled}
          rows={1}
          className="flex-1 resize-none rounded-xl border border-[#E8E8E4] bg-white px-4 py-2.5 text-sm text-[#0A0A0A] placeholder-[#AAA] outline-none focus:border-[#E85D2C] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          style={{ maxHeight: '160px' }}
        />
        <button
          onClick={handleSubmit}
          disabled={!canSend}
          aria-label="Send message"
          className="shrink-0 w-9 h-9 rounded-full flex items-center justify-center transition-colors cursor-pointer disabled:cursor-not-allowed"
          style={{
            backgroundColor: canSend ? '#E85D2C' : '#E8E8E4',
            color: canSend ? 'white' : '#AAA',
          }}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 13V3M8 3L3 8M8 3L13 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
      <p className="text-center text-[10px] text-[#CCC] mt-1.5">
        Enter to send · Shift+Enter for new line
      </p>
    </div>
  )
}
