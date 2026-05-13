import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import type { MessageItemProps } from '../types/components'

export default function MessageItem({ role, content, isStreaming }: MessageItemProps) {
  if (role === 'user') {
    return (
      <div className="flex justify-end px-4 py-1">
        <div className="max-w-[70%] rounded-2xl rounded-br-md bg-[#E85D2C] text-white px-4 py-2.5 text-sm whitespace-pre-wrap break-words shadow-sm">
          {content}
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start px-4 py-1">
      <div className="max-w-[70%] rounded-2xl rounded-bl-md bg-white border border-[#E8E8E4] px-4 py-2.5 text-sm text-[#0A0A0A] prose prose-sm prose-neutral max-w-none shadow-sm">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeHighlight]}
        >
          {isStreaming ? content + ' ▍' : content}
        </ReactMarkdown>
      </div>
    </div>
  )
}
