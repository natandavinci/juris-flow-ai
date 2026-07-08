"""
Monta o conteúdo do alerta (assunto + corpo) a partir do resultado do
grafo. Não sabe nada sobre SMTP -- só sabe transformar dado em texto.
"""

from src.models.schemas import ClassificacaoPublicacao, PublicacaoDJEN


def montar_assunto(
    publicacao: PublicacaoDJEN,
    classificacao: ClassificacaoPublicacao,
    data_limite: str | None,
) -> str:
    processo = publicacao.numero_processo_mascara or publicacao.numero_processo

    if classificacao.tem_prazo and data_limite:
        return f"⚠️ Prazo até {data_limite[:10]} -- Processo {processo}"
    if classificacao.tem_prazo:
        return f"📋 Ação requerida (prazo não especificado) -- Processo {processo}"
    return f"ℹ️ Nova publicação, sem prazo -- Processo {processo}"


def montar_corpo(
    publicacao: PublicacaoDJEN,
    classificacao: ClassificacaoPublicacao,
    data_limite: str | None,
) -> str:
    linhas = [
        f"Processo: {publicacao.numero_processo}",
        f"Tribunal: {publicacao.sigla_tribunal or 'não informado'}",
        f"Órgão: {publicacao.nome_orgao or 'não informado'}",
        "",
        f"Resumo: {classificacao.resumo_acao}",
        "",
    ]

    if data_limite:
        linhas.append(f"Prazo estimado (A CONFIRMAR): {data_limite}")
        linhas.append(
            "Este prazo foi calculado automaticamente e pode não "
            "considerar feriados locais/forenses. Confirme antes de agir."
        )
        linhas.append("")

    if not classificacao.confianca_alta:
        linhas.append(
            "⚠️ ATENÇÃO: a IA teve baixa confiança nesta classificação. "
            "Revise o texto original com atenção redobrada."
        )
        linhas.append("")

    if publicacao.link:
        linhas.append(f"Documento original: {publicacao.link}")

    linhas.append("")
    linhas.append("--- Texto completo da publicação ---")
    linhas.append(publicacao.texto)

    return "\n".join(linhas)