# garajes/config.py
import os
from dotenv import load_dotenv

# Cargar las variables de .env
load_dotenv()

# Parámetros de búsqueda
PRECIO_MAXIMO = float(os.getenv("PRECIO_MAXIMO", 95.0))
AREA_MINIMA = int(os.getenv("AREA_MINIMA", 20))
RADIO_KM = float(os.getenv("RADIO_KM", 1.0))
CENTRO_DIRECCION = os.getenv("CENTRO_DIRECCION", "Tu Dirección, Ciudad, País")

# Configuración de email
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Configuración de Twilio para WhatsApp
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

# Otras configuraciones, como el nombre de la BD
DB_NAME = "anuncios.db"
