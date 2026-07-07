
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


class ClassificacaoPublicacao(BaseModel):
    """
    Saída estruturada da IA ao interpretar o texto de uma publicação.

    Esse é o contrato que força o LLM a responder de um jeito que o
    resto do sistema consegue processar de forma confiável -- em vez
    de receber um parágrafo solto e precisar re-interpretar ele de
    novo com regex/heurística.
    """

    tem_prazo: bool = Field(
        description=(
            "True se a publicação exige alguma ação da parte dentro de "
            "um prazo (ex: contestar, recorrer, manifestar-se). False "
            "para despacho de mero expediente, sentença sem prazo de "
            "ação imediata, ou publicação meramente informativa."
        )
    )
    prazo_dias: int | None = Field(
        default=None,
        description=(
            "Número de dias do prazo mencionado no texto, se houver. "
            "None se tem_prazo=False ou se o texto não especificar."
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
            "tiver certeza razoável sobre tem_prazo/prazo_dias. Nesses "
            "casos, é preferível marcar False a arriscar um palpite."
        )
    )