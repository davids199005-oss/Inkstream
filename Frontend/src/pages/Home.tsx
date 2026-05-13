import { useEffect } from 'react'
import { useConversations } from '../hooks/useConversations'
import { useChat } from '../hooks/useChat'
import Sidebar from '../components/Sidebar'
import MessageList from '../components/MessageList'
import ChatInput from '../components/ChatInput'

export default function Home() {
  const convs = useConversations()
  const chat = useChat(convs.activeId, convs.updateTitle)

  useEffect(() => {
    const init = async () => {
      const list = await convs.fetchAll()
      if (list.length === 0) {
        await convs.create()
      } else {
        convs.setActive(list[0].id)
      }
    }
    init()
  }, [])

  return (
    <div className="flex h-full">
      <Sidebar
        conversations={convs.conversations}
        activeId={convs.activeId}
        onSelect={id => convs.setActive(id)}
        onCreate={convs.create}
        onDelete={convs.remove}
      />
      <div className="flex flex-col flex-1 min-h-0 min-w-0">
        {convs.activeId ? (
          <>
            <MessageList
              messages={chat.messages}
              assistantDraft={chat.assistantDraft}
              isStreaming={chat.isStreaming}
            />
            {chat.error && (
              <p className="px-4 py-2 text-xs text-red-500 text-center">{chat.error}</p>
            )}
            <ChatInput
              onSend={chat.sendMessage}
              isStreaming={chat.isStreaming}
              disabled={!convs.activeId}
            />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <p className="text-sm text-[#AAA] font-mono">Select or create a conversation</p>
          </div>
        )}
      </div>
    </div>
  )
}
