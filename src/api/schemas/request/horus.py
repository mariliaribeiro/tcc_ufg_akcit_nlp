from typing import Optional

from pydantic import BaseModel, Field


class HorusMedicineStockRequest(BaseModel):
    codigo_uf: Optional[str] = Field(
        default=None,
        description="Filtra pelo Código IBGE da Unidade da Federação à qual pertence o estabelecimento",
    )
    codigo_municipio: Optional[str] = Field(
        default=None,
        description="Filtra pelo Código IBGE do município ao qual pertence o estabelecimento",
    )
    codigo_cnes: Optional[str] = Field(
        default=None,
        description="Filtra pelo Código CNES do estabelecimento",
    )
    data_posicao_estoque: Optional[str] = Field(
        default=None,
        description="Filtra pela Data da posição de estoque informada. Formato: AAAA-MM-DD. Exemplo: 2024-02-21",
    )
    codigo_catmat: Optional[str] = Field(
        default=None,
        description="Filtra pelo Código CATMAT com unidade de fornecimento do item em estoque",
    )
    sigla_programa_saude: Optional[str] = Field(
        default=None,
        description="Filtra pela Sigla do programa de Saúde vinculado ao item",
    )
    tipo_produto: Optional[str] = Field(
        default=None,
        description="Filtra pela Sigla do Tipo do produto em estoque",
    )
    sigla_sistema_origem: Optional[str] = Field(
        default=None,
        description="Filtra pela Sigla do Sistema de origem do dado",
    )
    limit: int = Field(
        default=100,
        description="Quantidade de itens retornados por página. Deve ser menor ou igual 20",
    )
    offset: int = Field(
        default=0,
        description="Número da página de itens que deve ser retornada. Observação: As páginas iniciam a contagem a partir de 0 (zero), por exemplo: offset=0",
    )
