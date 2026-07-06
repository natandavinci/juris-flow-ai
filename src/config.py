import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    oab_numero: str
    oab_uf: str
    dias_retroativos: int

def get_config() -> Config:
    oab_numero = os.getenv("ADVOGADO_OAB_NUMERO")
    oab_uf = os.getenv("ADVOGADO_OAB_UF")

    if not oab_numero or not oab_uf:
        raise ValueError(
            "ADVOGADO_OAB_NUMERO e ADVOGADO_OAB_UF precisam estar definidos "
        )
    
    return Config(
        oab_numero=oab_numero,
        oab_uf= oab_uf,
        dias_retroativos=int(os.getenv("DJEN_DIAS_RETROATIVOS", "7"))
    )