import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Play, Square, RefreshCw, Download, Activity, FileText } from 'lucide-react'
import './App.css'

const API_BASE_URL = 'https://5000-ijc7gnx0ckiyiifuadaoj-a1790518.manusvm.computer/api/mining'

function App() {
  const [miningStatus, setMiningStatus] = useState({
    is_running: false,
    processed_count: 0,
    target_count: 50,
    current_medicine: null,
    logs: []
  })
  const [results, setResults] = useState({ total_found: 0, medicines: [] })
  const [isLoading, setIsLoading] = useState(false)

  // Função para buscar o status da mineração
  const fetchStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/status`)
      const data = await response.json()
      setMiningStatus(data)
    } catch (error) {
      console.error('Erro ao buscar status:', error)
    }
  }

  // Função para buscar os resultados
  const fetchResults = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/results`)
      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Erro ao buscar resultados:', error)
    }
  }

  // Função para iniciar a mineração
  const startMining = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_count: 50 })
      })
      if (response.ok) {
        fetchStatus()
      }
    } catch (error) {
      console.error('Erro ao iniciar mineração:', error)
    }
    setIsLoading(false)
  }

  // Função para parar a mineração
  const stopMining = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/stop`, {
        method: 'POST'
      })
      if (response.ok) {
        fetchStatus()
      }
    } catch (error) {
      console.error('Erro ao parar mineração:', error)
    }
    setIsLoading(false)
  }

  // Atualizar status automaticamente
  useEffect(() => {
    fetchStatus()
    fetchResults()
    
    const interval = setInterval(() => {
      fetchStatus()
      if (!miningStatus.is_running) {
        fetchResults()
      }
    }, 3000)

    return () => clearInterval(interval)
  }, [miningStatus.is_running])

  const progressPercentage = (miningStatus.processed_count / miningStatus.target_count) * 100

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Cabeçalho */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Sistema de Mineração de Bulas ANVISA
          </h1>
          <p className="text-gray-600">
            Automatização da coleta de bulas de medicamentos da ANVISA
          </p>
        </div>

        {/* Controles Principais */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5" />
              Controle da Mineração
            </CardTitle>
            <CardDescription>
              Inicie ou pare o processo de mineração de bulas
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4">
              <Button
                onClick={startMining}
                disabled={miningStatus.is_running || isLoading}
                className="flex items-center gap-2"
              >
                <Play className="h-4 w-4" />
                Iniciar Mineração
              </Button>
              <Button
                onClick={stopMining}
                disabled={!miningStatus.is_running || isLoading}
                variant="destructive"
                className="flex items-center gap-2"
              >
                <Square className="h-4 w-4" />
                Parar Mineração
              </Button>
              <Button
                onClick={fetchStatus}
                variant="outline"
                className="flex items-center gap-2"
              >
                <RefreshCw className="h-4 w-4" />
                Atualizar
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {miningStatus.processed_count}
                </div>
                <div className="text-sm text-blue-800">Bulas Encontradas</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {miningStatus.target_count}
                </div>
                <div className="text-sm text-green-800">Meta</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <Badge variant={miningStatus.is_running ? "default" : "secondary"}>
                  {miningStatus.is_running ? "Em Execução" : "Parado"}
                </Badge>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Progresso</span>
                <span>{Math.round(progressPercentage)}%</span>
              </div>
              <Progress value={progressPercentage} className="w-full" />
            </div>

            {miningStatus.current_medicine && (
              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="text-sm font-medium text-yellow-800">
                  Processando: {miningStatus.current_medicine}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Tabs para Logs e Resultados */}
        <Tabs defaultValue="logs" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="logs">Logs da Execução</TabsTrigger>
            <TabsTrigger value="results">Resultados</TabsTrigger>
          </TabsList>

          <TabsContent value="logs">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Logs da Execução
                </CardTitle>
                <CardDescription>
                  Acompanhe o progresso da mineração em tempo real
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96 w-full border rounded-md p-4">
                  {miningStatus.logs.length > 0 ? (
                    <div className="space-y-1">
                      {miningStatus.logs.map((log, index) => (
                        <div
                          key={index}
                          className="text-sm font-mono text-gray-700 border-b border-gray-100 pb-1"
                        >
                          {log}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center text-gray-500 py-8">
                      Nenhum log disponível
                    </div>
                  )}
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="results">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Download className="h-5 w-5" />
                  Resultados da Mineração
                </CardTitle>
                <CardDescription>
                  Medicamentos processados com bulas encontradas
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="mb-4">
                  <Badge variant="outline" className="text-lg px-3 py-1">
                    Total: {results.total_found} medicamentos
                  </Badge>
                </div>
                <ScrollArea className="h-96 w-full">
                  {results.medicines.length > 0 ? (
                    <div className="space-y-3">
                      {results.medicines.map((medicine, index) => (
                        <div
                          key={index}
                          className="p-4 border border-gray-200 rounded-lg bg-white"
                        >
                          <div className="font-medium text-gray-900 mb-2">
                            {medicine.product_name}
                          </div>
                          <div className="text-sm text-gray-600 space-y-1">
                            {medicine.professional_leaflet && (
                              <div>📄 Bula Profissional: {medicine.professional_leaflet}</div>
                            )}
                            {medicine.patient_leaflet && (
                              <div>📋 Bula Paciente: {medicine.patient_leaflet}</div>
                            )}
                            {medicine.processing_date && (
                              <div>🕒 Processado em: {new Date(medicine.processing_date).toLocaleString('pt-BR')}</div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center text-gray-500 py-8">
                      Nenhum resultado disponível
                    </div>
                  )}
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App
