SYSTEM_TEMPLATE = """
Extraia da pergunta abaixo o nome do medicamento, o nome do município (ou cidade) e a sigla da UF (estado brasileiro). 
Retorne um JSON com as chaves: 'medicamento', 'nome_municipio', 'codigo_municipio', 'uf'. 
Se não encontrar algum valor, retorne string vazia para aquele campo.

Human: {question}
"""

CONTEXT = """
# Structured data:
{structured_data}
"""
