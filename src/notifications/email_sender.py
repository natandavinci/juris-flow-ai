import smtplib
from email.message import EmailMessage


def enviar_email(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    destinatario: str,
    assunto: str,
    corpo: str,
) -> None:
    mensagem = EmailMessage()
    mensagem["From"] = smtp_user
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto
    mensagem.set_content(corpo)

    # starttls (porta 587) em vez de SSL direto (porta 465)
    with smtplib.SMTP(smtp_host, smtp_port) as servidor:
        servidor.starttls()
        servidor.login(smtp_user, smtp_password)
        servidor.send_message(mensagem)