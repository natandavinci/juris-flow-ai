from pydantic import BaseModel, ConfigDict, Field


class PublicacaoDJEN(BaseModel):

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    id_publicacao: int = Field(alias="id")
    numero_processo: str = Field(alias="numero_processo")
    texto: str = Field(alias="texto")
    data_disponibilizacao: str = Field(alias="data_disponibilizacao")
    hash_comunicacao: str = Field(alias="hash")
    sigla_tribunal: str | None = Field(default=None, alias="siglaTribunal")
    tipo_comunicacao: str | None = Field(default=None, alias="tipoComunicacao")
    nome_orgao: str | None = Field(default=None, alias="nomeOrgao")
    link: str | None = Field(default=None, alias="link")