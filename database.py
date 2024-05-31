import os
from pymongo import MongoClient


try:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client['python']
    print("Conexión a la base de datos establecida correctamente.")
except Exception as e:
    print("Error al conectar a la base de datos:", e)