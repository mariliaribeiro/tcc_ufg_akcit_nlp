# Metodologia de Mineração de Bulas da ANVISA para Construção de Graph RAG

## 1. Introdução

Este documento descreve a metodologia utilizada para minerar e estruturar bulas de medicamentos registrados na Agência Nacional de Vigilância Sanitária (ANVISA), com o objetivo de alimentar uma base de dados para um sistema de Recuperação Aumentada por Geração (RAG) baseada em grafos. A metodologia aqui apresentada segue os princípios do método científico, organizando as etapas de coleta, filtragem, processamento e armazenamento dos dados de forma sistemática.

---

## 2. Objetivo

Construir uma base estruturada de bulas de medicamentos ativos e relevantes no Brasil, utilizando dados públicos da ANVISA, com vistas ao uso em aplicações baseadas em inteligência artificial para recuperação de informação e suporte à pesquisa científica e profissional.

---

## 3. Materiais e Métodos

### 3.1 Fonte de Dados Primária

A principal fonte de dados utilizada é o **conjunto de dados de medicamentos registrados no Brasil**, disponibilizado em:

> https://dados.gov.br/dados/conjuntos-dados/medicamentos-registrados-no-brasil

#### Estrutura dos Dados:

O arquivo CSV contém os seguintes campos:

- `TIPO_PRODUTO`
- `NOME_PRODUTO`
- `DATA_FINALIZACAO_PROCESSO`
- `CATEGORIA_REGULATORIA`
- `NUMERO_REGISTRO_PRODUTO`
- `DATA_VENCIMENTO_REGISTRO`
- `NUMERO_PROCESSO`
- `CLASSE_TERAPEUTICA`
- `EMPRESA_DETENTORA_REGISTRO`
- `SITUACAO_REGISTRO`
- `PRINCIPIO_ATIVO`

---

### 3.2 Pré-processamento dos Dados

1. **Importação no MongoDB**:  
   Todos os dados do CSV são importados para uma base de dados MongoDB para facilitar a consulta e manipulação.

2. **Filtragem por Situação**:  
   São considerados apenas medicamentos com `SITUACAO_REGISTRO = "Ativo"`.

3. **Seleção dos mais relevantes**:  
   Seleção dos **Top 50 medicamentos mais utilizados no Brasil** (critério de relevância determinado com base em fontes complementares de consumo ou uso clínico — **essa etapa pode ser revisitada conforme novas métricas de relevância sejam incorporadas**).

---

### 3.3 Coleta das Bulas

A coleta das bulas é realizada diretamente do **portal de bulas da ANVISA**:

> https://consultas.anvisa.gov.br/#/bulario

#### Processo Automatizado (Crawler):

- Linguagem: Python
- Mecanismo: Navegação automatizada e parsing HTML
- Entrada: Campo `NOME_PRODUTO` do medicamento é utilizado como parâmetro de busca no campo “Medicamento” do formulário de pesquisa da ANVISA.
- Verificação: Conforme verificado em 14/06/2025, o portal não utiliza CAPTCHA, o que permite a automação da coleta.
- Saída:
  - Para cada medicamento encontrado, são coletadas **duas versões da bula**:
    - **Profissional de saúde** (prioritária)
    - **Paciente**
  - As bulas são salvas:
    - Em arquivos PDF, armazenados em pastas nomeadas com o `NUMERO_REGISTRO_PRODUTO`.
    - Em formato **base64**, armazenadas na collection `bulas` do MongoDB com os metadados correspondentes.

---

### 3.4 Armazenamento dos Dados

O sistema de armazenamento é estruturado conforme:

- Banco de dados: **MongoDB**
- Collections:
  - `medicamentos`: contém os dados brutos e tratados do CSV original.
  - `bulas`: contém os documentos PDF em base64 e seus respectivos metadados, como tipo de bula (profissional/paciente), link de origem, timestamp de download e nome do produto.

---

## 4. Resultados Esperados

- Construção de uma base de dados confiável e atualizada com bulas de medicamentos ativos no Brasil.
- Criação de um grafo de conhecimento que relacione produtos, princípios ativos, empresas, classes terapêuticas e textos das bulas.
- Base para implementação de um sistema Graph RAG (Retrieval-Augmented Generation) focado em consultas por profissionais de saúde e pesquisadores.

---

## 5. Considerações Éticas

- Todos os dados utilizados são públicos e de livre acesso.
- Não são coletados dados pessoais ou sensíveis.
- O uso da base é destinado a fins científicos e tecnológicos, respeitando os termos de uso do portal ANVISA.

---

## 6. Referências

- Agência Nacional de Vigilância Sanitária (ANVISA): https://www.gov.br/anvisa
- Dados Abertos: https://dados.gov.br/dados/conjuntos-dados/medicamentos-registrados-no-brasil
- Portal de Bulas ANVISA: https://consultas.anvisa.gov.br/#/bulario
