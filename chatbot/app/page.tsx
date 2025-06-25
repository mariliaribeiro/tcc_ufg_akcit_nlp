"use client"

import type React from "react"
import { useChat } from "ai/react"
import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Mic, MicOff, Trash2, Send, Bot, User, Sun, Moon, Github, ChevronDown } from "lucide-react"
import { cn } from "@/lib/utils"

interface SpeechRecognition extends EventTarget {
  continuous: boolean
  interimResults: boolean
  lang: string
  start(): void
  stop(): void
  abort(): void
}

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList
  resultIndex: number
}

declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition
    webkitSpeechRecognition: new () => SpeechRecognition
    webkitSpeechRecognition: new () => SpeechRecognition
  }
}

const quickMessages = [
  "Qual o estoque de dipirona na cidade de Goiana?",
  "Qual o princípio ativo do DRAMIN?",
  "Quais cidades têm estoque positivo de loratadina?",
  "Quais os medicamentos que posso pesquisar?",
]

export default function ChatbotMedicamentos() {
  const { messages, input, handleInputChange, handleSubmit, setMessages, isLoading } = useChat()
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState("")
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [showQuickMessages, setShowQuickMessages] = useState(true)
  const recognitionRef = useRef<SpeechRecognition | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Mostrar mensagens rápidas apenas quando não há histórico
    setShowQuickMessages(messages.length === 0)
  }, [messages])

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition()
        recognitionRef.current.continuous = true
        recognitionRef.current.interimResults = true
        recognitionRef.current.lang = "pt-BR"

        recognitionRef.current.onresult = (event: SpeechRecognitionEvent) => {
          let finalTranscript = ""
          for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
              finalTranscript += event.results[i][0].transcript
            }
          }
          if (finalTranscript) {
            setTranscript(finalTranscript)
            handleInputChange({ target: { value: finalTranscript } } as any)
          }
        }

        recognitionRef.current.onerror = () => {
          setIsListening(false)
        }

        recognitionRef.current.onend = () => {
          setIsListening(false)
        }
      }
    }
  }, [handleInputChange])

  const toggleListening = () => {
    if (!recognitionRef.current) return

    if (isListening) {
      recognitionRef.current.stop()
      setIsListening(false)
    } else {
      recognitionRef.current.start()
      setIsListening(true)
      setTranscript("")
    }
  }

  const clearHistory = () => {
    setMessages([])
    setShowQuickMessages(true)
  }

  const sendQuickMessage = (message: string) => {
    setShowQuickMessages(false)
    handleInputChange({ target: { value: message } } as any)
    const syntheticEvent = {
      preventDefault: () => {},
      target: { value: message },
    } as any
    handleSubmit(syntheticEvent)
  }

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode)
  }

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (isListening) {
      recognitionRef.current?.stop()
    }
    setShowQuickMessages(false)
    handleSubmit(e)
  }

  return (
    <div className={cn("min-h-screen transition-colors duration-300", isDarkMode ? "bg-gray-900" : "bg-white")}>
      {/* Header */}
      <header
        className={cn(
          "border-b px-6 py-4 transition-colors duration-300",
          isDarkMode ? "bg-gray-800 border-gray-700" : "bg-white border-gray-200",
        )}
      >
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center">
              <div className="w-4 h-4 bg-white rounded-sm"></div>
            </div>
            <span
              className={cn(
                "text-xl font-semibold transition-colors duration-300",
                isDarkMode ? "text-white" : "text-black",
              )}
            >
              GraphRAG TCC
            </span>
          </div>

          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" className="gap-2">
              <span className={cn("transition-colors duration-300", isDarkMode ? "text-white" : "text-black")}>
                Português (Brasil)
              </span>
              <ChevronDown className="h-4 w-4" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => window.open("https://github.com/mariliaribeiro/tcc_ufg_akcit_nlp", "_blank")}
            >
              <Github
                className={cn("h-5 w-5 transition-colors duration-300", isDarkMode ? "text-white" : "text-black")}
              />
            </Button>

            <Button variant="ghost" size="icon" onClick={toggleTheme}>
              {isDarkMode ? <Sun className="h-5 w-5 text-white" /> : <Moon className="h-5 w-5 text-black" />}
            </Button>

            <Button className="bg-blue-600 hover:bg-blue-700 text-white">b</Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6 max-w-4xl">
        {/* Chat Interface */}
        <Card
          className={cn(
            "shadow-xl border transition-colors duration-300",
            isDarkMode ? "bg-gray-800 border-gray-700" : "bg-white border-gray-200",
          )}
        >
          <CardHeader
            className={cn(
              "border-b transition-colors duration-300",
              isDarkMode ? "border-gray-700" : "border-gray-200",
            )}
          >
            <div className="flex items-center justify-between">
              <CardTitle
                className={cn(
                  "flex items-center gap-2 transition-colors duration-300",
                  isDarkMode ? "text-white" : "text-black",
                )}
              >
                <Bot className="h-5 w-5 text-blue-600" />
                Consulta de Estoque de Medicamentos
              </CardTitle>
              <Button
                variant="ghost"
                size="sm"
                onClick={clearHistory}
                className={cn(
                  "transition-colors duration-300",
                  isDarkMode ? "text-white hover:bg-gray-700" : "text-black hover:bg-gray-100",
                )}
                disabled={messages.length === 0}
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Limpar
              </Button>
            </div>
          </CardHeader>

          <CardContent className="h-[500px] overflow-y-auto p-4 space-y-4">
            {showQuickMessages && (
              <div className="space-y-3">
                <div
                  className={cn(
                    "text-center mb-6 transition-colors duration-300",
                    isDarkMode ? "text-gray-300" : "text-gray-600",
                  )}
                >
                  <Bot className="h-16 w-16 mx-auto mb-4 text-blue-600" />
                  <p className="text-lg font-medium">Olá! Como posso ajudar?</p>
                  <p className="text-sm">Escolha uma das opções abaixo ou digite sua pergunta</p>
                </div>

                <div className="flex flex-wrap gap-2 justify-center">
                  {quickMessages.map((message, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      className={cn(
                        "text-left justify-start h-auto p-4 transition-all duration-200 inline-block w-auto",
                        isDarkMode
                          ? "border-gray-600 text-gray-300 bg-gray-800 hover:bg-gray-700 hover:border-blue-500 hover:text-white"
                          : "border-gray-300 text-black bg-white hover:bg-blue-50 hover:border-blue-300",
                      )}
                      onClick={() => sendQuickMessage(message)}
                      disabled={isLoading}
                    >
                      <span className="text-sm">{message}</span>
                    </Button>
                  ))}
                </div>
              </div>
            )}

            {!showQuickMessages &&
              messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "flex gap-3 max-w-[80%]",
                    message.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto",
                  )}
                >
                  <div
                    className={cn(
                      "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
                      message.role === "user" ? "bg-blue-600 text-white" : "bg-blue-600 text-white",
                    )}
                  >
                    {message.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                  </div>
                  <div
                    className={cn(
                      "rounded-2xl px-4 py-3 shadow-sm",
                      message.role === "user"
                        ? "bg-blue-600 text-white rounded-br-md"
                        : isDarkMode
                          ? "bg-gray-700 text-white rounded-bl-md"
                          : "bg-gray-100 text-black rounded-bl-md",
                    )}
                  >
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              ))}

            {isLoading && !showQuickMessages && (
              <div className="flex gap-3 max-w-[80%] mr-auto">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center">
                  <Bot className="h-4 w-4" />
                </div>
                <div
                  className={cn(
                    "rounded-2xl rounded-bl-md px-4 py-3 shadow-sm",
                    isDarkMode ? "bg-gray-700" : "bg-gray-100",
                  )}
                >
                  <div className="flex space-x-1">
                    <div
                      className={cn("w-2 h-2 rounded-full animate-bounce", isDarkMode ? "bg-gray-400" : "bg-gray-500")}
                    ></div>
                    <div
                      className={cn("w-2 h-2 rounded-full animate-bounce", isDarkMode ? "bg-gray-400" : "bg-gray-500")}
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className={cn("w-2 h-2 rounded-full animate-bounce", isDarkMode ? "bg-gray-400" : "bg-gray-500")}
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </CardContent>

          <CardFooter
            className={cn(
              "border-t pt-4 transition-colors duration-300",
              isDarkMode ? "bg-gray-800 border-gray-700" : "bg-gray-50 border-gray-200",
            )}
          >
            <form onSubmit={onSubmit} className="flex w-full gap-2">
              <div className="flex-1 relative">
                <Input
                  value={input}
                  onChange={handleInputChange}
                  placeholder="Digite sua pergunta sobre medicamentos..."
                  className={cn(
                    "pr-12 h-12 transition-colors duration-300",
                    isDarkMode
                      ? "bg-gray-700 border-gray-600 text-white placeholder:text-gray-400 focus:border-blue-500"
                      : "bg-white border-gray-300 text-black focus:border-blue-500",
                  )}
                  disabled={isLoading}
                />
                {isListening && (
                  <Badge className="absolute right-14 top-1/2 -translate-y-1/2 bg-red-500 text-white animate-pulse">
                    Ouvindo...
                  </Badge>
                )}
              </div>

              <Button
                type="button"
                variant="outline"
                size="icon"
                onClick={toggleListening}
                className={cn(
                  "h-12 w-12 transition-all duration-200",
                  isListening
                    ? "bg-red-500 hover:bg-red-600 text-white border-red-500"
                    : isDarkMode
                      ? "border-gray-600 text-gray-300 bg-gray-800 hover:bg-gray-700 hover:text-white"
                      : "border-gray-300 text-black hover:bg-gray-100",
                )}
                disabled={!recognitionRef.current}
              >
                {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
              </Button>

              <Button
                type="submit"
                className="h-12 px-6 bg-blue-600 hover:bg-blue-700 text-white transition-all duration-200"
                disabled={isLoading || !input.trim()}
              >
                <Send className="h-4 w-4 mr-2" />
                Enviar
              </Button>
            </form>
          </CardFooter>
        </Card>

        {/* Footer */}
        <div
          className={cn(
            "text-center mt-6 text-sm transition-colors duration-300",
            isDarkMode ? "text-gray-400" : "text-gray-600",
          )}
        >
          <p>Desenvolvido por Ana Cabral e Marília Ribeiro • UFG PLN 2025</p>
        </div>
      </div>
    </div>
  )
}
