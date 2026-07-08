"""
Ponto de entrada da V1: busca publicações do DJEN, filtra as novas,
roda cada uma pelo grafo (classificação + cálculo de prazo), envia um
alerta por email, e só então marca como processada.
"""

from src.config import get_config
from src.graph.build import build_graph
from src.ingestion.djen_client import buscar_publicacoes
from src.notifications.email_sender import enviar_email
from src.notifications.formatter import montar_assunto, montar_corpo
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
        data_limite = resultado.get("data_limite_calculada")

        print("=" * 60)
        print(f"Processo: {publicacao.numero_processo}")
        print(f"Tem prazo? {classificacao.tem_prazo}")
        print(f"Resumo: {classificacao.resumo_acao}")
        if data_limite:
            print(f"Prazo estimado (a confirmar!): {data_limite}")
        if not classificacao.confianca_alta:
            print("⚠️  IA com baixa confiança -- revisar manualmente.")

        assunto = montar_assunto(publicacao, classificacao, data_limite)
        corpo = montar_corpo(publicacao, classificacao, data_limite)

        try:
            enviar_email(
                smtp_host=config.smtp_host,
                smtp_port=config.smtp_port,
                smtp_user=config.smtp_user,
                smtp_password=config.smtp_password,
                destinatario=config.email_destinatario,
                assunto=assunto,
                corpo=corpo,
            )
            print("✅ Email de alerta enviado.")
        except Exception as erro:
            # IMPORTANTE: se o envio falhar, NÃO marcamos como
            # processada -- assim, na próxima execução, o sistema
            # tenta avisar de novo em vez de perder o alerta em
            # silêncio. Prefira reenviar um alerta duplicado a nunca
            # enviar um alerta importante.
            print(f"❌ Falha ao enviar email: {erro}")
            print("   Publicação NÃO marcada como processada -- será")
            print("   reprocessada e reenviada na próxima execução.")
            continue

        marcar_como_processada(
            publicacao.hash_comunicacao, publicacao.numero_processo
        )


if __name__ == "__main__":
    main()