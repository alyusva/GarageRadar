import os
from telegram import Bot
from config.settings import Config
from src.aws.secrets_manager import get_secret

class TelegramNotifier:
    def __init__(self):
        secrets = get_secret(Config.SECRET_NAME)
        self.bot = Bot(token=secrets['TELEGRAM_TOKEN'])
        self.chat_id = secrets['TELEGRAM_CHAT_ID']
        
    def send(self, message):
        try:
            self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Error enviando mensaje de Telegram: {str(e)}")

def format_garage_message(garage):
    return f"""
    🚗 *Nuevo garaje encontrado!*
    
    *Título:* {garage['titulo']}
    *Precio:* {garage['precio']}€
    *Ubicación:* {garage['ubicacion']}
    [Ver anuncio]({garage['enlace']})
    """