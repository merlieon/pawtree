import type { Message } from '../types'

interface Props {
    message: Message
}

function ChatBubble({ message }: Props) {
  return (
    <div
      style={{
        alignSelf: message.role === 'user' ? 'flex-end' : 'flex-start',
        background: message.role === 'user' ? '#4a4a4a' : '#2a2a2a',
        color: 'white',
        borderRadius: '12px',
        padding: '8px 12px',
        maxWidth: '75%',
        fontSize: '14px',
        wordBreak: 'break-word',
        overflowWrap: 'break-word',
      }}
    >
      {message.content}
    </div>
  )
}

export default ChatBubble