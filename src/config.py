import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    DEBUG: bool = os.getenv('DEBUG') == 'True'

settings = Settings()
