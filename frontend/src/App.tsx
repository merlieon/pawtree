import type { PedigreeNode } from './types'
import { useState, useEffect } from 'react'
import PedigreeBox from './PedigreeBox'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

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
    <div>
      <div>
        {tree && <PedigreeBox node={tree} />}
      </div>
      <div>
      {messages.map((msg, i) => (
        <div key={i}>
          <strong>{msg.role}:</strong> {msg.content}
        </div>
      ))}
      </div>
      <input
      value={input}
      onChange={(e => setInput(e.target.value))}
      placeholder='Fråga om en hundras...'
      />
      <button onClick={send}>Skicka</button>
      </div>
      
  )
}

export default App