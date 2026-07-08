import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    oab_numero: str
    oab_uf: str
    dias_retroativos: int
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    email_destinatario: str

def get_config() -> Config:
    oab_numero = os.getenv("ADVOGADO_OAB_NUMERO")
    oab_uf = os.getenv("ADVOGADO_OAB_UF")

    if not oab_numero or not oab_uf:
        raise ValueError(
            "ADVOGADO_OAB_NUMERO e ADVOGADO_OAB_UF precisam estar definidos "
        )
    
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_destinatario = os.getenv("EMAIL_DESTINATARIO")
 
    if not smtp_user or not smtp_password or not email_destinatario:
        raise ValueError(
            "SMTP_USER, SMTP_PASSWORD e EMAIL_DESTINATARIO precisam estar "
            "definidos no .env para o envio de alertas funcionar."
        )
 
    return Config(
        oab_numero=oab_numero,
        oab_uf=oab_uf,
        dias_retroativos=int(os.getenv("DJEN_DIAS_RETROATIVOS", "7")),
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_user=smtp_user,
        smtp_password=smtp_password,
        email_destinatario=email_destinatario,
    )