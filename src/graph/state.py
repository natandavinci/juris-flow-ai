from typing import TypedDict

from src.models.schemas import ClassificacaoPublicacao, PublicacaoDJEN


class GraphState(TypedDict):
    publicacao: PublicacaoDJEN
    classificacao: ClassificacaoPublicacao | None
    data_limite_calculada: str | None  # formato ISO (YYYY-MM-DD), ou None