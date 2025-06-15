# Projeto de Mineração de Bulas da ANVISA

Este projeto automatiza a coleta de bulas de medicamentos a partir do site da ANVISA e salva os dados em um banco de dados MongoDB, além de fornecer uma interface de usuário para controle e visualização do processo.

## Funcionalidades

- **Mineração de Dados**: Coleta bulas de medicamentos do site da ANVISA (`https://consultas.anvisa.gov.br/#/bulario`).
- **Persistência de Dados**: Salva informações dos medicamentos e caminhos das bulas (PDFs) em um banco de dados MongoDB.
- **Interface de Usuário (Web)**: Permite iniciar, parar e monitorar o processo de mineração, visualizar logs em tempo real e consultar os resultados.
- **Modo Headless**: A mineração é realizada em segundo plano, sem a necessidade de abrir o navegador visualmente.
- **Tratamento de Erros**: Inclui tratamento de exceções e logs para monitoramento.
- **Controle de Fluxo**: Garante intervalos entre as requisições para evitar bloqueios.

## Estrutura do Projeto

```
ufg_pln_tcc/
├── anvisa_miner_api/        # Backend da aplicação (Flask)
│   ├── src/
│   │   ├── main.py          # Ponto de entrada do Flask
│   │   └── routes/          # Rotas da API
│   │       └── mining.py    # Rotas para controle da mineração
│   └── venv/                # Ambiente virtual do Python para o backend
├── anvisa_miner_frontend/   # Frontend da aplicação (React)
│   ├── src/
│   │   ├── App.jsx          # Componente principal do React
│   │   └── App.css          # Estilos CSS
│   ├── index.html           # Arquivo HTML principal
│   └── ...                  # Outros arquivos do React
├── data/                    # Pasta para salvar os arquivos PDF das bulas
├── database.py              # Módulo para conexão e operações com MongoDB
├── scraper.py               # Módulo para scraping com Selenium
└── main.py                  # Script principal de mineração (execução via CLI, não usado pela API)
```

## Requisitos

Para executar este projeto, você precisará ter instalado:

- **Python 3.x**
- **Node.js e pnpm** (para o frontend React)
- **MongoDB** (servidor rodando localmente ou acessível)
- **Google Chrome** (navegador)

## Configuração e Execução

Siga os passos abaixo para configurar e executar o projeto:

### 1. Clonar o Repositório (se aplicável)

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
```

### 2. Configurar o Backend (Flask)

```bash
cd ufg_pln_tcc/anvisa_miner_api
source venv/bin/activate  # Ativar o ambiente virtual
pip install -r requirements.txt # Instalar dependências (se houver um requirements.txt)
pip install pymongo selenium webdriver_manager flask-cors # Instalar dependências adicionais
python src/main.py
```

O servidor Flask será iniciado na porta `5000` (ou outra porta configurada).

### 3. Configurar o Frontend (React)

Em um novo terminal:

```bash
cd ufg_pln_tcc/anvisa_miner_frontend
pnpm install # Instalar dependências
pnpm run dev --host
```

O servidor de desenvolvimento do React será iniciado na porta `5173` (ou outra porta configurada).

### 4. Acessar a Interface

Abra seu navegador e acesse a URL do frontend (geralmente `http://localhost:5173/` ou a URL exposta pelo `service_expose_port`).

### 5. Iniciar a Mineração

Na interface web, clique no botão "Iniciar Mineração". Você poderá acompanhar o progresso e os logs em tempo real.

## Observações

- O diretório `data/` será criado na raiz do projeto (`ufg_pln_tcc/data`) para armazenar os PDFs das bulas.
- O script `main.py` na raiz do projeto (`ufg_pln_tcc/main.py`) é para execução via linha de comando e não é utilizado pela API Flask. A lógica de mineração foi integrada diretamente ao backend da API para controle via interface.
- Certifique-se de que o servidor MongoDB esteja em execução e acessível.