import type { Message } from '../types'
import ChatBubble from './ChatBubble'


interface Props {
    messages: Message[]
    input: string
    onInputChange: (value: string) => void
    onSend: () => void
}

function ChatCard({ messages, input, onInputChange, onSend }: Props) {
  return (
    <div style={{
      border: '0.5px solid #444',
      borderRadius: '12px',
      padding: '1rem',
      display: 'flex',
      flexDirection: 'column',
      height: '500px',          // fast höjd så input hamnar kvar nere
    }}>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
        flex: 1,                 // tar allt tillgängligt utrymme
        overflowY: 'auto',       // scrollar om många meddelanden
        marginBottom: '12px',
      }}>
        {messages.map((msg, i) => (
          <ChatBubble key={i} message={msg} />
        ))}
      </div>

      <div style={{ display: 'flex', gap: '8px' }}>
        <input
          value={input}
          onChange={(e) => onInputChange(e.target.value)}
          placeholder="Fråga om en hundras..."
          style={{ flex: 1 }}
        />
        <button onClick={onSend}>Skicka</button>
      </div>
    </div>
  )
}

export default ChatCard