from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PublicacaoDJEN(BaseModel):

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    id_publicacao: int = Field(alias="id")
    numero_processo: str = Field(alias="numero_processo")
    texto: str = Field(alias="texto")
    # Nome real do campo na API (confirmado em execução real) -- não é
    # "data_publicacao" como eu havia assumido antes de testar.
    data_disponibilizacao: str = Field(alias="data_disponibilizacao")
    hash_comunicacao: str = Field(alias="hash")
    sigla_tribunal: str | None = Field(default=None, alias="siglaTribunal")
    tipo_comunicacao: str | None = Field(default=None, alias="tipoComunicacao")
    nome_orgao: str | None = Field(default=None, alias="nomeOrgao")
    link: str | None = Field(default=None, alias="link")


class ClassificacaoPublicacao(BaseModel):

    tem_prazo: bool = Field(
        description=(
            "True se a publicação exige alguma ação da parte dentro de "
            "um prazo (ex: contestar, recorrer, manifestar-se). False "
            "para despacho de mero expediente, sentença sem prazo de "
            "ação imediata, ou publicação meramente informativa."
        )
    )
    prazo_quantidade: int | None = Field(
        default=None,
        description=(
            "Número mencionado no texto para o prazo (ex: 5, 15, 48). "
            "None se tem_prazo=False ou se o texto não especificar."
        ),
    )
    unidade_prazo: Literal["dias_uteis", "horas"] | None = Field(
        default=None,
        description=(
            "Unidade do prazo_quantidade. 'dias_uteis' é o padrão "
            "processual mais comum (ex: 'prazo de 15 dias'). Use "
            "'horas' quando o texto especificar explicitamente horas "
            "(ex: '48 horas antes da sessão'). Nunca assuma dias_uteis "
            "por padrão se o texto disser horas -- são cálculos "
            "diferentes e confundir os dois pode gerar um prazo errado."
        ),
    )
    resumo_acao: str = Field(
        description=(
            "Resumo em 1-2 frases, em português simples (sem juridiquês "
            "desnecessário), do que precisa ser feito e por quem."
        )
    )
    confianca_alta: bool = Field(
        description=(
            "False se o texto for ambíguo, incompleto, ou se você não "
            "tiver certeza razoável sobre tem_prazo/prazo_quantidade/"
            "unidade_prazo. Nesses casos, é preferível marcar False a "
            "arriscar um palpite."
        )
    )