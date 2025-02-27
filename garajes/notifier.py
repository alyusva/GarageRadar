# garajes/notifier.py
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from .config import (
    SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, TWILIO_TO
)

def enviar_email(anuncios):
    """Envía un email con los anuncios nuevos."""
    if not anuncios:
        return
    body = "Se han encontrado nuevos anuncios de garajes:\n\n"
    for ad in anuncios:
        body += f"{ad['titulo']} - {ad['precio']}€/mes - {ad['area']}m²\n{ad['url']}\n\n"
    msg = MIMEText(body, "plain")
    msg["Subject"] = "Nuevos anuncios de garajes disponibles"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], msg.as_string())
        print("Email enviado correctamente.")
    except Exception as e:
        print("Error al enviar el email:", e)

def enviar_whatsapp(anuncios):
    """Envía un mensaje de WhatsApp con los anuncios nuevos usando Twilio."""
    if not anuncios:
        return
    body = "Nuevos garajes:\n"
    for ad in anuncios:
        body += f"{ad['titulo']} - {ad['precio']}€/mes - {ad['area']}m²\n{ad['url']}\n"
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        print("Mensaje de WhatsApp enviado, SID:", message.sid)
    except Exception as e:
        print("Error al enviar WhatsApp:", e)
