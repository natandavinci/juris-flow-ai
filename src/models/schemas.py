from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PublicacaoDJEN(BaseModel):

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    id_publicacao: int = Field(alias="id")
    numero_processo: str = Field(alias="numero_processo")
    numero_processo_mascara: str | None = Field(
        default=None, alias="numeroprocessocommascara"
    )
    texto: str = Field(alias="texto")
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
    referencia_prazo: Literal["disponibilizacao", "evento_futuro"] | None = Field(
        default=None,
        description=(
            "Como contar o prazo. 'disponibilizacao': conta PARA FRENTE "
            "a partir da data em que esta publicação foi disponibilizada "
            "(o padrão mais comum, ex: 'manifeste-se em 5 dias'). "
            "'evento_futuro': conta PARA TRÁS a partir de uma data/hora "
            "de um evento futuro mencionado NO PRÓPRIO TEXTO (ex: "
            "'até 48 horas antes do início da sessão do dia 13/07/2026 "
            "às 09:00' -- aqui o prazo NÃO tem relação com a data de "
            "disponibilização, e sim com a data do evento citado)."
        ),
    )
    data_evento_futuro: str | None = Field(
        default=None,
        description=(
            "Preencha APENAS quando referencia_prazo='evento_futuro'. "
            "Data e hora do evento mencionado no texto (audiência, "
            "sessão de julgamento, perícia), no formato "
            "'YYYY-MM-DDTHH:MM:SS'. Extraia exatamente do texto -- "
            "nunca calcule ou estime essa data."
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