import type { Message } from './models'

export interface StreamCallbacks {
  onUserMessage: (msg: Message) => void
  onToken: (text: string) => void
  onDone: (messageId: string, title: string | null) => void
  onError: (message: string) => void
}
