from datetime import date, timedelta

import requests

from pydantic import ValidationError

from src.models.schemas import PublicacaoDJEN

BASE_URL = "https://comunicaapi.pje.jus.br/api/v1/comunicacao"
 
 
def buscar_publicacoes(
    oab_numero: str, oab_uf: str, dias_retroativos: int = 7
) -> list[PublicacaoDJEN]:
    
    data_fim = date.today()
    data_inicio = data_fim - timedelta(days=dias_retroativos)
 
    params = {
        "numeroOab": oab_numero,
        "ufOab": oab_uf,
        "dataDisponibilizacaoInicio": data_inicio.isoformat(),
        "dataDisponibilizacaoFim": data_fim.isoformat(),
    }
 
    resposta = requests.get(BASE_URL, params=params, timeout=30)
    resposta.raise_for_status()
    dados = resposta.json()

    itens_brutos = dados.get("items", dados if isinstance(dados, list) else [])
 
    publicacoes: list[PublicacaoDJEN] = []
    for item in itens_brutos:
        try:
            publicacoes.append(PublicacaoDJEN.model_validate(item))
        except ValidationError as erro:
            print(f"[aviso] publicação com formato inesperado, pulando: {erro}")
 
    return publicacoes