"""
Nós do grafo. Cada função aqui recebe o GraphState e devolve um dict
com apenas os campos que ela alterou -- é assim que o LangGraph
espera que um nó se comporte.
"""

from datetime import date, datetime, timedelta

from langsmith import traceable

from src.graph.state import GraphState
from src.llm import get_chat_model
from src.models.schemas import ClassificacaoPublicacao
from src.utils.calendario import calcular_data_limite, calcular_limite_horas

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

Preste atenção especial em DOIS pontos que costumam ser confundidos:

1) UNIDADE do prazo: prazos processuais tradicionais são em dias \
(geralmente úteis), mas alguns atos específicos (ex: sustentação \
oral) são contados em horas corridas.

2) REFERÊNCIA do prazo -- este é o ponto mais importante: a maioria \
dos prazos conta PARA FRENTE a partir de quando esta publicação foi \
disponibilizada (referencia_prazo='disponibilizacao'). MAS alguns \
textos mencionam um evento futuro (sessão de julgamento, audiência) \
e pedem uma ação ANTES desse evento (ex: 'até 48 horas antes do \
início da sessão do dia 13/07/2026 às 09:00') -- nesse caso é \
referencia_prazo='evento_futuro', e você precisa extrair a data/hora \
exata desse evento do texto, em data_evento_futuro. NUNCA trate um \
prazo 'antes de um evento' como se fosse contado a partir da \
disponibilização -- são cálculos opostos (um soma, o outro subtrai) \
e confundir os dois já causou um erro real de mais de uma semana \
numa execução anterior deste sistema.

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
    if not (
        classificacao
        and classificacao.tem_prazo
        and classificacao.prazo_quantidade
        and classificacao.unidade_prazo
        and classificacao.referencia_prazo
    ):
        return "fim"

    if (
        classificacao.referencia_prazo == "evento_futuro"
        and not classificacao.data_evento_futuro
    ):
        return "fim"

    return "calcular_prazo"


@traceable(name="calcular_prazo")
def node_calcular_prazo(state: GraphState) -> dict:
    classificacao = state["classificacao"]
    publicacao = state["publicacao"]

    if classificacao.referencia_prazo == "evento_futuro":
        data_evento = datetime.fromisoformat(classificacao.data_evento_futuro)
        horas = (
            classificacao.prazo_quantidade
            if classificacao.unidade_prazo == "horas"
            else classificacao.prazo_quantidade * 24
        )
        data_limite = data_evento - timedelta(hours=horas)
        return {"data_limite_calculada": data_limite.isoformat()}

    
    data_disponibilizacao = date.fromisoformat(publicacao.data_disponibilizacao)

    if classificacao.unidade_prazo == "dias_uteis":
        data_limite = calcular_data_limite(
            data_inicio=data_disponibilizacao,
            prazo_dias=classificacao.prazo_quantidade,
        )
        return {"data_limite_calculada": data_limite.isoformat()}

    limite_datetime = calcular_limite_horas(
        data_inicio=data_disponibilizacao,
        prazo_horas=classificacao.prazo_quantidade,
    )
    return {"data_limite_calculada": limite_datetime.isoformat()}