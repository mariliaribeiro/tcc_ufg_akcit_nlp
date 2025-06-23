from typing import List, Optional

from pydantic import BaseModel, Field


class HorusMedicineStockParams(BaseModel):
    codigo_uf: int = Field(
        description="Código IBGE da Unidade da Federação à qual pertence o estabelecimento",
    )
    uf: str = Field(description="Unidade da Federação à qual pertence o estabelecimento")
    codigo_municipio: Optional[int] = Field(
        description="Filtra pelo Código IBGE do município ao qual pertence o estabelecimento",
    )
    municipio: Optional[str] = Field(
        description="Município ao qual pertence o estabelecimento",
    )
    codigo_cnes: Optional[int] = Field(
        description="Código CNES do estabelecimento",
    )
    data_posicao_estoque: Optional[str] = Field(
        description="Data da posição de estoque informada. Formato: AAAA-MM-DD. Exemplo: 2024-02-21",
    )
    codigo_catmat: Optional[str] = Field(
        description="Código CATMAT com unidade de fornecimento do item em estoque",
    )
    descricao_produto: Optional[str] = Field(
        description="Descrição do produto",
    )
    quantidade_estoque: Optional[int] = Field(
        description="Quantidade do produto em estoque",
    )
    numero_lote: Optional[str] = Field(
        description="Número do lote",
    )
    data_validade: Optional[str] = Field(
        description="Data de validade informada. Formato: AAAA-MM-DD HH:MM:SS-TZ. Exemplo: 2024-02-21 00:00:00-03",
    )
    tipo_produto: Optional[str] = Field(
        description="Tipo do produto",
    )
    sigla_programa_saude: Optional[str] = Field(
        description="Sigla do programa de Saúde vinculado ao item",
    )
    descricao_programa_saude: Optional[str] = Field(
        description="Descrição do programa de Saúde vinculado ao item",
    )
    sigla_sistema_origem: Optional[str] = Field(
        description="Sigla do Sistema de origem do dado",
    )
    razao_social: Optional[str] = Field(
        description="Razão social",
    )
    nome_fantasia: Optional[str] = Field(
        description="Nome fantasia",
    )
    cep: Optional[str] = Field(
        description="CEP",
    )
    logradouro: Optional[str] = Field(
        description="Logradouro",
    )
    numero_endereco: Optional[str] = Field(
        description="Número do endereço",
    )
    bairro: Optional[str] = Field(
        description="Bairro",
    )
    telefone: Optional[str] = Field(
        description="Telefone",
    )
    latitude: Optional[float] = Field(description="Latitude")
    longitude: Optional[float] = Field(description="Longitude")
    email: Optional[str] = Field(
        description="E-mail",
    )


class HorusMedicineStockResponse(BaseModel):
    parametros: List[HorusMedicineStockParams]
