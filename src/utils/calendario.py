"""
Cálculo de data-limite de prazo processual.

LIMITAÇÃO CONHECIDA (importante para o advogado que for usar isso):
considera apenas sábados, domingos e feriados NACIONAIS fixos. Não
considera feriados estaduais/municipais, nem recesso forense (que
varia por tribunal). Por isso todo resultado desta função deve ser
tratado como uma ESTIMATIVA a confirmar por um humano antes de virar
uma decisão real de prazo -- nunca a fonte final de verdade.
"""

from datetime import date, timedelta

# Feriados nacionais fixos (data, sempre no mesmo dia todo ano).
# Feriados móveis (Carnaval, Páscoa, Corpus Christi) ficam de fora
FERIADOS_NACIONAIS_FIXOS = {
    (1, 1),   # Confraternização Universal
    (4, 21),  # Tiradentes
    (5, 1),   # Dia do Trabalho
    (9, 7),   # Independência
    (10, 12), # Nossa Senhora Aparecida
    (11, 2),  # Finados
    (11, 15), # Proclamação da República
    (12, 25), # Natal
}


def eh_feriado_nacional_fixo(dia: date) -> bool:
    return (dia.month, dia.day) in FERIADOS_NACIONAIS_FIXOS


def eh_dia_util(dia: date) -> bool:
    fim_de_semana = dia.weekday() >= 5  # 5=sábado, 6=domingo
    return not fim_de_semana and not eh_feriado_nacional_fixo(dia)


def calcular_data_limite(data_inicio: date, prazo_dias: int) -> date:
    """
    Conta `prazo_dias` dias úteis a partir de `data_inicio` (exclusive)
    e retorna a data-limite resultante.
    """
    dia_atual = data_inicio
    dias_contados = 0

    while dias_contados < prazo_dias:
        dia_atual += timedelta(days=1)
        if eh_dia_util(dia_atual):
            dias_contados += 1

    return dia_atual