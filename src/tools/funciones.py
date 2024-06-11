from src.schemas.user import user_schema
from src.schemas.product import product_schema
from src.models.UserModel import User
from src.models.ProductsModel import Product
import database as db

def search_user(field: str, key):

    try:
        user = db.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
    