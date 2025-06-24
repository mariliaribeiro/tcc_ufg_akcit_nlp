ALLOWED_NODES = [
    "Empresa",
    "Medicamento",
    "Fármaco",
    "Doença",
    "Paciente",
    "Profissão",
    "Consumo",
    "Frequência",
]

ALLOWED_RELATIONSHIPS = [
    "FORNECE",
    "INTERAÇÕES",
    "PERTENCE",
    "SEMELHANTE",
    "INDICAÇÕES",
    "COMPOSIÇÃO",
    "EFICÁCIA",
    "CONTRAINDICAÇÕES",
    "INTERAÇÕES MEDICAMENTOSAS",
    "ADVERTÊNCIAS E PRECAUÇÕES",
    "REAÇÕES ADVERSAS",
    "ADMINISTRAÇÃO",
    "REGISTRO",
    "PRODUZIDO",
]


IBGE_CODE_FOR_BRAZILIAN_UF = [
    {"nome": "Acre", "codigo": 12, "sigla": "AC"},
    {"nome": "Ceará", "codigo": 23, "sigla": "CE"},
    {"nome": "São Paulo", "codigo": 35, "sigla": "SP"},
    {"nome": "Paraná", "codigo": 41, "sigla": "PR"},
    {"nome": "Bahia", "codigo": 29, "sigla": "BA"},
    {"nome": "Goiás", "codigo": 52, "sigla": "GO"},
    {"nome": "Distrito Federal", "codigo": 53, "sigla": "DF"},
    {"nome": "Santa Catarina", "codigo": 42, "sigla": "BA"},
]

CATMAT_CODE = [
    {
        "principio_ativo": "Ibuprofeno",
        "codigo_catmat": "BR0332755-6",
        "concentracao": "100 mg/ml",
        "forma_farmaceutica": "Suspensão oral",
        "unidade_fornecimento": "Frasco 100 ml",
    },
    {
        "principio_ativo": "Paracetamol",
        "codigo_catmat": "BR0267778",
        "concentracao": "500 mg",
        "forma_farmaceutica": "Comprimido",
        "unidade_fornecimento": "Comprimido",
    },
    {
        "principio_ativo": "Esomeprazol, Magnésio",
        "codigo_catmat": "BR0274186",
        "concentracao": "20 mg",
        "forma_farmaceutica": "Cápsula",
        "unidade_fornecimento": "Cápsula",
    },
    {
        "principio_ativo": "Nimesulida",
        "codigo_catmat": "BR0273710",
        "concentracao": "100 mg",
        "forma_farmaceutica": "Comprimido",
        "unidade_fornecimento": "Comprimido",
    },
]

IBGE_CODE_FOR_BRAZILIAN_UF_TEXT = "\n".join(
    [
        f"- Nome do Estado (UF) = {i['nome']}, Sigla = {i['sigla']}, Código IBGE = {i['codigo']}"
        for i in IBGE_CODE_FOR_BRAZILIAN_UF
    ]
)
CATMAT_CODE_TEXT = "\n".join(
    [
        f"- Princípio ativo = {i['principio_ativo']}, Código CATMAT = {i['codigo_catmat']}"
        for i in CATMAT_CODE
    ]
)
