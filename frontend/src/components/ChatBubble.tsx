import type { Message } from '../types'
import './ChatBubble.css'

interface Props {
    message: Message
}

function ChatBubble({ message }: Props) {
  const modifier = message.role === 'user' ? 'chat-bubble--user' : 'chat-bubble--assistant'
  return <div className={`chat-bubble ${modifier}`}>{message.content}</div>
}

export default ChatBubble