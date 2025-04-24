'use client'
import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/cjs/styles/prism'

export default function ChatPage() {
  const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; text: string }[]>([])
  const [input, setInput] = useState('')
  const chatRef = useRef<HTMLDivElement>(null)

  const sendMessage = async () => {
    if (!input.trim()) return
  
    const newMessage = { sender: 'user', text: input }
    setMessages((prev) => [...prev, newMessage])
    const query = input
    setInput('')
  
    try {
      const response = await fetch('http://127.0.0.1:8000/api/py/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })
  
      const data = await response.json()
  
      if (!response.ok) throw new Error(data.detail || 'Something went wrong')
  
        const formatSources = (sources: string[]) => {
          if (!sources.length) return ''
          return sources
            .map((src) => {
              const isURL = src.startsWith('http')
              return isURL ? `<a href="${src}" class="underline text-blue-400" target="_blank">${src}</a>` : `<span>${src}</span>`
            })
            .join(', ')
        }
        
        const botReply = {
          sender: 'bot' as const,
          text: `**ChaiBot:**\n\n${data.Bot}\n\n${
            data.Sources?.length
              ? `**Sources:**\n${data.Sources.map((s) => `- [${s}](${s})`).join('\n')}`
              : ''
          }`,
        }
      setMessages((prev) => [...prev, botReply])
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: `⚠️ Error: ${err.message}` },
      ])
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') sendMessage()
  }

  useEffect(() => {
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages])

  return (
    <div className="flex flex-col h-screen  text-white ">
      <div className="title-wrapper sl-flex astro-kmkmnagf"> 
        <a href="/" className="site-title sl-flex astro-m46x6ez3">  
        <img className="light:sl-hidden print:hidden astro-m46x6ez3 pl-4 pt-4" alt="" src="https://chaidocs.vercel.app/_astro/chai-docs-white.CjIIo2Jk.png" width="180"  /> 
        <span className="sr-only astro-m46x6ez3" translate="no"> Chai aur Docs 
        </span> 
      </a>  
    </div>
      <div className="flex-grow overflow-y-auto p-4 space-y-2 scrollbar-thin scrollbar-thumb-zinc-600 scrollbar-track-zinc-900" ref={chatRef}>
        {messages.map((msg, i) => (
          // <div
          //   key={i}
          //   className={`max-w-lg p-3 rounded-xl w-fit ${
          //     msg.sender === 'user'
          //       ? 'ml-auto bg-zinc-200 text-black'
          //       : 'mr-auto bg-transparent'
          //   }`}
          // >
          //   {msg.text}
          // </div>
          <div
            key={i}
            className={`max-w-lg p-3 rounded-xl w-fit  mx-[25%] ${
              msg.sender === 'user'
                ? 'ml-auto bg-zinc-200 text-black'
                : 'mr-auto bg-transparent text-white'
            }`}
          >
            {msg.sender === 'bot' ? (
              <div className="prose prose-invert max-w-none">
              <ReactMarkdown
                components={{
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '')
                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={oneDark}
                        language={match[1]}
                        PreTag="div"
                        className="rounded-lg p-4"
                        {...props}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    ) : (
                      <code className="bg-zinc-900 rounded px-1 py-0.5 text-sm">{children}</code>
                    )
                  },
                  a({ href, children }) {
                    return (
                      <a href={href} className="text-blue-400 underline" target="_blank" rel="noopener noreferrer">
                        {children}
                      </a>
                    )
                  },
                }}
              >
                {msg.text}
              </ReactMarkdown>
              </div>
            ) : (
              msg.text
            )}
          </div>
        ))}
      </div>
      <div className="p-4 border-t border-zinc-700 mx-[25%]">
        <input
          type="text"
          className="w-full p-3 rounded-lg bg-zinc-800 text-white outline-none"
          placeholder="Send a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </div>
    </div>
  )
}