
from datetime import date

from langsmith import traceable

from src.graph.state import GraphState
from src.llm import get_chat_model
from src.models.schemas import ClassificacaoPublicacao
from src.utils.calendario import calcular_data_limite

PROMPT_CLASSIFICACAO = """\
Você é um assistente jurídico que analisa publicações do Diário de \
Justiça Eletrônico e identifica se elas exigem alguma ação da parte \
dentro de um prazo.

Analise o texto abaixo e preencha os campos solicitados. Se o texto \
for um despacho de mero expediente, uma publicação sem prazo de ação \
imediata, ou você não tiver certeza, marque tem_prazo=False e/ou \
confianca_alta=False -- é preferível admitir incerteza a arriscar um \
palpite errado, já que um erro aqui pode custar um prazo processual \
real para o advogado.

Texto da publicação:
---
{texto}
---
"""


@traceable(name="classificar_publicacao")
def node_classificar(state: GraphState) -> dict:
    publicacao = state["publicacao"]

    modelo = get_chat_model().with_structured_output(ClassificacaoPublicacao)
    prompt = PROMPT_CLASSIFICACAO.format(texto=publicacao.texto)

    resultado: ClassificacaoPublicacao = modelo.invoke(prompt)

    return {"classificacao": resultado}


def rotear_apos_classificacao(state: GraphState) -> str:
    """
    Função de roteamento condicional (não é um nó, é a "bifurcação").
    Decide se vale a pena calcular prazo ou encerrar por aqui.
    """
    classificacao = state["classificacao"]
    if classificacao and classificacao.tem_prazo and classificacao.prazo_dias:
        return "calcular_prazo"
    return "fim"


@traceable(name="calcular_prazo")
def node_calcular_prazo(state: GraphState) -> dict:
    classificacao = state["classificacao"]
    publicacao = state["publicacao"]

    data_disponibilizacao = date.fromisoformat(publicacao.data_disponibilizacao)
    data_limite = calcular_data_limite(
        data_inicio=data_disponibilizacao,
        prazo_dias=classificacao.prazo_dias,
    )

    return {"data_limite_calculada": data_limite.isoformat()}