import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuración de scraping
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) GarageRadar/1.0"
    MAX_PRICE = int(os.getenv("MAX_PRICE", 150))
    MIN_DIMENSIONS = (2.5, 5)  # Ancho x Largo
    LOCATION = os.getenv("LOCATION", "Madrid Centro")
    
    # AWS
    AWS_REGION = os.getenv("AWS_REGION", "eu-west-3")
    SECRET_NAME = os.getenv("SECRET_NAME", "garage-radar/secrets")
    
    # Notificaciones
    NOTIFICATION_METHODS = os.getenv("NOTIFICATION_METHODS", "telegram,email").split(",")
    
    @classmethod
    def get_db_url(cls):
        return f"sqlite:///{os.path.dirname(__file__)}/../garages.db"