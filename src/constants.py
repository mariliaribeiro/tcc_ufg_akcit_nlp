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
    {"nome": "Alagoas", "codigo": 27, "sigla": "AL"},
    {"nome": "Amapá", "codigo": 16, "sigla": "AP"},
    {"nome": "Amazonas", "codigo": 13, "sigla": "AM"},
    {"nome": "Bahia", "codigo": 29, "sigla": "BA"},
    {"nome": "Ceará", "codigo": 23, "sigla": "CE"},
    {"nome": "Distrito Federal", "codigo": 53, "sigla": "DF"},
    {"nome": "Espírito Santo", "codigo": 32, "sigla": "ES"},
    {"nome": "Goiás", "codigo": 52, "sigla": "GO"},
    {"nome": "Maranhão", "codigo": 21, "sigla": "MA"},
    {"nome": "Mato Grosso", "codigo": 51, "sigla": "MT"},
    {"nome": "Mato Grosso do Sul", "codigo": 50, "sigla": "MS"},
    {"nome": "Minas Gerais", "codigo": 31, "sigla": "MG"},
    {"nome": "Pará", "codigo": 15, "sigla": "PA"},
    {"nome": "Paraíba", "codigo": 25, "sigla": "PB"},
    {"nome": "Paraná", "codigo": 41, "sigla": "PR"},
    {"nome": "Pernambuco", "codigo": 26, "sigla": "PE"},
    {"nome": "Piauí", "codigo": 22, "sigla": "PI"},
    {"nome": "Rio de Janeiro", "codigo": 33, "sigla": "RJ"},
    {"nome": "Rio Grande do Norte", "codigo": 24, "sigla": "RN"},
    {"nome": "Rio Grande do Sul", "codigo": 43, "sigla": "RS"},
    {"nome": "Rondônia", "codigo": 11, "sigla": "RO"},
    {"nome": "Roraima", "codigo": 14, "sigla": "RR"},
    {"nome": "Santa Catarina", "codigo": 42, "sigla": "SC"},
    {"nome": "São Paulo", "codigo": 35, "sigla": "SP"},
    {"nome": "Sergipe", "codigo": 28, "sigla": "SE"},
    {"nome": "Tocantins", "codigo": 17, "sigla": "TO"},
]


CATMAT_CODE = [
    {
        "principio_ativo": "CLORIDRATO DE NAFAZOLINA",
        "codigo_catmat": "BR0272400-1",
	    "concentracao": "0,5 mg/ml",
	    "forma_farmaceutica": "Solução nasal",
	    "unidade_fornecimento": "Frasco 30 ml"
    },
    {
        "principio_ativo": "CLORIDRATO DE METFORMINA",
        "codigo_catmat": "BR0465425",
	    "concentracao": "850 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "BESILATO DE ANLODIPINO +  LOSARTANA POTÁSSICA",
        "codigo_catmat": "BR0272434U0042",
	    "concentracao": "5 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "LEVOTIROXINA SÓDICA",
        "codigo_catmat": "BR0268123U0042",
	    "concentracao": "50 mcg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "NIMESULIDA",
        "codigo_catmat": "BR0273710",
	    "concentracao": "100 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "DIPIRONA",
        "codigo_catmat": "BR0267203U0042",
	    "concentracao": "500 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "LORATADINA",
        "codigo_catmat": "BR0273466U0042",
	    "concentracao": "10 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "BUTILBROMETO DE ESCOPOLAMINA",
        "codigo_catmat": "BR0270620",
	    "concentracao": "10 mg + 250 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "MALEATO DE DEXCLORFENIRAMINA",
        "codigo_catmat": "BR0452409",
	    "concentracao": "4 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "CLORIDRATO DE BROMEXINA",
        "codigo_catmat": "BR0269821",
	    "concentracao": "1,6 mg/ml",
	    "forma_farmaceutica": "Xarope",
	    "unidade_fornecimento": "Frasco 120 ml"
    },
    {
        "principio_ativo": "ETINILESTRADIOL +  LEVONORGESTREL",
        "codigo_catmat": "BR0272789U0042",
	    "concentracao": "0,15 mg + 0,03 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Cartela com 21 comprimidos"
    },
    {
        "principio_ativo": "ATENOLOL",
        "codigo_catmat": "BR0267517U0042",
	    "concentracao": "50 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "IBUPROFENO",
        "codigo_catmat": "BR0267676U0042",
	    "concentracao": "600 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "CLONAZEPAM",
        "codigo_catmat": "BR0270120U0086",
	    "concentracao": "2,5 mg/ml",
	    "forma_farmaceutica": "Solução Oral",
	    "unidade_fornecimento": "Frasco 20 ml"
    },
    {
        "principio_ativo": "GLIBENCLAMIDA",
        "codigo_catmat": "BBR0267671U0042",
	    "concentracao": "5 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "FLUCONAZOL",
        "codigo_catmat": "BR0267662U0041",
	    "concentracao": "150 mg",
	    "forma_farmaceutica": "Cápsula",
	    "unidade_fornecimento": "Cápsula"
    },
    {
        "principio_ativo": "NISTATINA +  ÓXIDO DE ZINCO",
        "codigo_catmat": "BR0279297-2",
	    "concentracao": "100.000 + 200 UI + mg/g",
	    "forma_farmaceutica": "Creme",
	    "unidade_fornecimento": "Bisnaga 60 g"
    },
    {
        "principio_ativo": "SOLUCAO DE SALBUTAMOL +  SULFATO DE SALBUTAMOL",
        "codigo_catmat": "BR0294887U0084",
	    "concentracao": "100 mcg/dose",
	    "forma_farmaceutica": "Aerossol Oral (Inalador)",
	    "unidade_fornecimento": "Frasco com 200 doses"
    },
    {
        "principio_ativo": "LOSARTANA POTÁSSICA",
        "codigo_catmat": "BR0268856U0042",
	    "concentracao": "50 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "DEXPANTENOL",
        "codigo_catmat": "BR0392423",
	    "concentracao": "50 mg/g",
	    "forma_farmaceutica": "Gel Oftálmico",
	    "unidade_fornecimento": "Bisnaga 10 g"
    },
    {
        "principio_ativo": "ALBENDAZOL",
        "codigo_catmat": "BR0267506U0042",
	    "concentracao": "400 mg",
	    "forma_farmaceutica": "Comprimido Mastigável",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "SIMETICONA",
        "codigo_catmat": "BR0412965",
	    "concentracao": "75 mg/ml",
	    "forma_farmaceutica": "Solução Oral (Gotas)",
	    "unidade_fornecimento": "Frasco 15 ml"
    },
    {
        "principio_ativo": "CETOPROFENO",
        "codigo_catmat": "BR0340101",
	    "concentracao": "100 mg",
	    "forma_farmaceutica": "Pó Liófilo para Suspensão Injetável Endovenosa",
	    "unidade_fornecimento": "Frasco-ampola"
    },
    {
        "principio_ativo": "OMEPRAZOL SÓDICO",
        "codigo_catmat": "BR0268160",
	    "concentracao": "40 mg",
	    "forma_farmaceutica": "Pó para solução injetável",
	    "unidade_fornecimento": "Frasco-ampola"
    },
    {
        "principio_ativo": "CARMELOSE SÓDICA",
        "codigo_catmat": "BR0305428-3",
	    "concentracao": "5 mg/ml",
	    "forma_farmaceutica": "Solução Oftálmica",
	    "unidade_fornecimento": "Frasco 10 ml"
    },
    {
        "principio_ativo": "NAPROXENO",
        "codigo_catmat": "BR0273703",
	    "concentracao": "500 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "FOSFATO SÓDICO DE PREDNISOLONA +  PREDNISOLONA",
        "codigo_catmat": "BBR0268151U0062",
	    "concentracao": "1 mg/ml",
	    "forma_farmaceutica": "Solução Oral",
	    "unidade_fornecimento": "Frasco 100 ml"
    },
    {
        "principio_ativo": "BUDESONIDA",
        "codigo_catmat": "BR0266707U0066",
	    "concentracao": "64 mcg/dose",
	    "forma_farmaceutica": "Suspensão Nasal",
	    "unidade_fornecimento": "Frasco 120 doses"
    },
    {
        "principio_ativo": "FENOBARBITAL",
        "codigo_catmat": "BR0267660U0042",
	    "concentracao": "100 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "SUCCINATO DE METOPROLOL",
        "codigo_catmat": "BR0276658U0042",
	    "concentracao": "100 mg",
	    "forma_farmaceutica": "Comprimido de liberação prolongada",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "PANTOPRAZOL SÓDICO SESQUI-HIDRATADO",
        "codigo_catmat": "BR0267892",
	    "concentracao": "40 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "SACCHAROMYCES BOULARDII +  SACCHAROMYCES BOULARDII - 17",
        "codigo_catmat": "BR0275989",
	    "concentracao": "200 mg/g",
	    "forma_farmaceutica": "Pó para solução oral",
	    "unidade_fornecimento": "Envelope"
    },
    {
        "principio_ativo": "IVERMECTINA",
        "codigo_catmat": "BR0273328U0042",
	    "concentracao": "6 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "ETINILESTRADIOL +  LEVONORGESTREL",
        "codigo_catmat": "BR0268370U0042",
	    "concentracao": "200 mg",
	    "forma_farmaceutica": "Comprimido",
	    "unidade_fornecimento": "Comprimido"
    },
    {
        "principio_ativo": "ÁCIDO ASCÓRBICO",
        "codigo_catmat": "BR0271687",
	    "concentracao": "100 mg/mL",
	    "forma_farmaceutica": "Solução injetável",
	    "unidade_fornecimento": "Ampola 5 mL"
    },
    {
        "principio_ativo": "CEFALEXINA MONOIDRATADA",
        "codigo_catmat": "BR0331555U0062",
	    "concentracao": "50 mg/mL",
	    "forma_farmaceutica": "Suspensão Oral",
	    "unidade_fornecimento": "Frasco"
    },
    {
        "principio_ativo": "CLORIDRATO  DE ONDANSETRONA DI-HIDRATADO",
        "codigo_catmat": "BR0305751",
	    "concentracao": "50 mg/mL",
	    "forma_farmaceutica": "Suspensão oral",
        "volume": "100 mL"
    },
    {
        "principio_ativo": "ENOXAPARINA SÓDICA",
        "codigo_catmat": "BR0268455",
	    "concentracao": "80 mg/0,8 mL",
	    "forma_farmaceutica": "Solução injetável",
	    "unidade_fornecimento": "Seringa preenchida"
    },
    {
        "principio_ativo": "DIMENIDRINATO",
        "codigo_catmat": "BR0272335",
	    "concentracao": "25 mg + 5 mg/mL",
	    "forma_farmaceutica": "Solução oral (gotas)",
        "volume": "20 mL"
    },
    {
        "principio_ativo": "HIDROCLOROTIAZIDA",
        "codigo_catmat": "BR0267674U0042",
        "concentracao": "25 mg",
        "forma_farmaceutica": "Comprimido",
        "unidade_fornecimento":  "Comprimido"
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
