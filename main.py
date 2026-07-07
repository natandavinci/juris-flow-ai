from src.config import get_config
from src.ingestion.djen_client import buscar_publicacoes
from src.storage.db import init_db, ja_processada, marcar_como_processada


def main() -> None:
    config = get_config()
    init_db()

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
        print("=" * 60)
        print(f"Processo: {publicacao.numero_processo}")
        print(f"Data: {publicacao.data_disponibilizacao}")
        print(f"Texto: {publicacao.texto[:300]}...")
        marcar_como_processada(
            publicacao.hash_comunicacao, publicacao.numero_processo
        )


if __name__ == "__main__":
    main()