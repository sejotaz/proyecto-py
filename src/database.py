from pymongo import MongoClient
from src.config import settings
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Database:
    def __init__(self):
        try:
            # Configurar la conexión con un tiempo de espera mayor
            self.client = MongoClient(settings.DATABASE_URL, serverSelectionTimeoutMS=50000)
            # Probar la conexión
            self.client.admin.command('ping')
            self.database = self.client.get_database('python')
            logger.info("Conexión a la base de datos exitosa.")
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            raise e

db = Database().database
