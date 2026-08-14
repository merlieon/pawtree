import type { PedigreeNode, Message } from './types'
import { useState } from 'react'
import ChatBubble from './components/ChatBubble'
import PedigreeBox from './components/PedigreeBox'
import './App.css'

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
    <div className="app">
      <div className="app__header">
        <p className="app__title">Pawtree</p>
        <p className="app__subtitle">Stamtavla och rasrådgivning</p>
      </div>

<div className="app__main">
  <div className="app__chat">
    <div className="app__messages">
      <div className="app__message-list">
        {messages.map((msg, i) => <ChatBubble key={i} message={msg} />)}
      </div>
    </div>
  
    <div className="app__input-bar">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Fråga om en hundras..."
      />
      <button onClick={send}>Skicka</button>
    </div>
  </div>
    <div className="app__divider" />
    {tree && (
      <div className="app__tree">
        <p className="app__tree-title">Stamtavla</p>
        <PedigreeBox node={tree} />
      </div>
    )}
</div>
    </div>
  )
}

export default App