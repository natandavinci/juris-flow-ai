"""
Ponto de entrada da V1: busca publicações do DJEN, filtra as novas,
roda cada uma pelo grafo (classificação + cálculo de prazo), e
imprime o resultado interpretado no console.

Ainda sem Telegram -- isso é a próxima etapa, depois de validarmos
que a classificação e o prazo calculado fazem sentido.
"""

from src.config import get_config
from src.graph.build import build_graph
from src.ingestion.djen_client import buscar_publicacoes
from src.storage.db import init_db, ja_processada, marcar_como_processada


def main() -> None:
    config = get_config()
    init_db()
    grafo = build_graph()

    print(
        f"Buscando publicações do DJEN para OAB {config.oab_numero}/"
        f"{config.oab_uf}, últimos {config.dias_retroativos} dias..."
    )

    publicacoes = buscar_publicacoes(
        oab_numero=config.oab_numero,
        oab_uf=config.oab_uf,
        dias_retroativos=config.dias_retroativos,
    )

    print(f"Total retornado pela API: {len(publicacoes)}")

    novas = [p for p in publicacoes if not ja_processada(p.hash_comunicacao)]
    print(f"Novas (ainda não vistas): {len(novas)}\n")

    for publicacao in novas:
        resultado = grafo.invoke({"publicacao": publicacao})
        classificacao = resultado["classificacao"]

        print("=" * 60)
        print(f"Processo: {publicacao.numero_processo}")
        print(f"Tem prazo? {classificacao.tem_prazo}")
        print(f"Resumo: {classificacao.resumo_acao}")
        if resultado.get("data_limite_calculada"):
            print(
                f"Prazo estimado (a confirmar!): "
                f"{resultado['data_limite_calculada']}"
            )
        if not classificacao.confianca_alta:
            print("⚠️  IA com baixa confiança -- revisar manualmente.")

        marcar_como_processada(
            publicacao.hash_comunicacao, publicacao.numero_processo
        )


if __name__ == "__main__":
    main()