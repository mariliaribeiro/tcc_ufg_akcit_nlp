export const maxDuration = 30

export async function POST(req: Request) {
  try {
    const { messages, audio } = await req.json()

    // Preparar dados para enviar para a API externa
    const lastMessage = messages[messages.length - 1]
    const requestBody = {
      text: lastMessage?.content || "",
      audio: audio || null,
    }

    // Fazer requisição para a API externa
    const response = await fetch("https://tccgraphrag.brkbot.com.br/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: process.env.TCC_API_KEY || "API-KEY-HERE",
      },
      body: JSON.stringify(requestBody),
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    const data = await response.json()

    // Retornar resposta no formato esperado pelo useChat
    return new Response(
      JSON.stringify({
        content: data.response || data.message || "Resposta não disponível",
      }),
      {
        headers: { "Content-Type": "application/json" },
      },
    )
  } catch (error) {
    console.error("Erro na API:", error)
    return new Response(
      JSON.stringify({
        content: "Desculpe, ocorreu um erro ao processar sua solicitação. Tente novamente.",
      }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      },
    )
  }
}
