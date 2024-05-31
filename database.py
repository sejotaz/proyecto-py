import os
from pymongo import MongoClient
import certifi


try:
    client = MongoClient(os.getenv("DATABASE"), tlsCAFile=certifi.where())
    db = client['python']
    print("Conexión a la base de datos establecida correctamente.")
except Exception as e:
    print("Error al conectar a la base de datos:", e)