import type { PedigreeNode, Message } from './types'
import { useState } from 'react'
import ChatCard from './components/ChatCard'
import ChatBubble from './components/ChatBubble'
import PedigreeBox from './components/PedigreeBox'



function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [tree, setTree] = useState<PedigreeNode | null>(null)

  async function send() {
    if (!input.trim()) return
    const userMessage: Message = { role: 'user', content: input }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setInput('')

    const res = await fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input, history: messages }),
    })

    const data = await res.json()
    const assistantMessage: Message = { role: 'assistant', content: data.reply }
    setMessages([...newMessages, assistantMessage])

    if (data.pedigree) {
      setTree(data.pedigree)
    }
  }
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100%', maxWidth: '900px', margin: '0 auto', boxSizing: 'border-box', overflowX: 'hidden' }}>

      {/* Header */}
      <div style={{ padding: '1.5rem 1rem 0' }}>
        <p style={{ fontSize: '18px', fontWeight: 500, margin: 0 }}>Pawtree</p>
        <p style={{ fontSize: '13px', color: '#888', margin: 0 }}>Stamtavla och rasrådgivning</p>
      </div>

      {/* Trädkort — FAST, egen sektion */}
      {tree && (
        <div style={{
          border: '0.5px solid #444',
          borderRadius: '12px',
          padding: '1rem',
          margin: '1rem 1rem 0',
          maxHeight: '280px',
          overflow: 'auto',
        }}>
          <PedigreeBox node={tree} />
        </div>
      )}

      {/* Meddelanden — enda delen som scrollar */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '1rem', minWidth: 0 }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {messages.map((msg, i) => <ChatBubble key={i} message={msg} />)}
        </div>
      </div>

      {/* Input — fast botten */}
      <div style={{ display: 'flex', gap: '8px', padding: '1rem', borderTop: '0.5px solid #444' }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Fråga om en hundras..." style={{ flex: 1, minWidth: 0 }} />
        <button onClick={send}>Skicka</button>
      </div>
    </div>
  )
}

export default App