from src.database import db
from src.models.UserModel import User  # Asegúrate de que la ruta y el nombre del modelo sean correctos
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

collection: Collection = db["users"]

# Crear índices únicos para el campo "username" y "email"
collection.create_index("username", unique=True)
collection.create_index("email", unique=True)

class AuthController:
    @staticmethod
    def create_user(user: User) -> User:
        user_dict = user.dict(by_alias=True)
        try:
            collection.insert_one(user_dict)
        except DuplicateKeyError as e:
            raise ValueError(f"Error al crear el usuario: {e}")
        return User(**user_dict)
