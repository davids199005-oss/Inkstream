import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'

interface Props {
  role: 'user' | 'assistant'
  content: string
  isStreaming?: boolean
}

export default function MessageItem({ role, content, isStreaming }: Props) {
  if (role === 'user') {
    return (
      <div className="flex justify-end px-4 py-1">
        <p className="max-w-[70%] text-sm font-semibold text-[#0A0A0A] text-right whitespace-pre-wrap break-words">
          {content}
        </p>
      </div>
    )
  }

  return (
    <div className="flex justify-start px-4 py-1">
      <div className="max-w-[70%] text-sm text-[#0A0A0A] prose prose-sm prose-neutral max-w-none">
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
