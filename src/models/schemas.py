from pydantic import BaseModel, ConfigDict, Field

class PublicacaoDJEN(BaseModel):
    model_config = ConfigDict(

        extra="ignore",
        populate_by_name=True,
    )

    id_publicacao: int = Field(alias="id")
    numero_processo : str = Field(alias="numero_processo")
    texto: str = Field(alias="texto")
    data_publicacao: str = Field(alias="data_publicacao")
    hash_comunicacao: str = Field(alias="hash")
    tribunal_id: int | None = Field(default=None, alias="tribunal_id")
    link: str | None = Field(default=None, alias="link")