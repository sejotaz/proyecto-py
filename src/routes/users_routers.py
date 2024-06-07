from fastapi import APIRouter, HTTPException, status
from src.models.UserModel import User, UserUpdate
from src.schemas.user import user_schema, users_schema
from database import db, client
from bson import ObjectId
from typing import Dict, Optional

router = APIRouter(prefix="/users", tags=["users"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}})

#Obtener todos los usuarios
@router.get("/query", response_model=list[User])
async def users():
    return users_schema(db.users.find({"isRemove": False}))


#Obtener un usuario por id
@router.get("/query/{id}")
async def users(id: str):
    return search_user("_id", ObjectId(id))

#O
@router.get("/query/")
async def users(id: str):
    return search_user("_id", id)


#Crear un usuario
@router.post("/create", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    try:
        user_dict = user.model_dump()
        del user_dict["id"]

        id = db.users.insert_one(user_dict).inserted_id
        # id = result

        new_user = user_schema(db.users.find_one({"_id": id}))

        return User(**new_user)
    except Exception as e:
        print("Error al crear el usuario:", e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error al crear el usuario")


@router.patch("/update/{id}", response_model=User)
async def update_user(id: str ,user: UserUpdate):

    update_data: Dict[str, Optional[str]] = user.model_dump(exclude_unset=True)
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")

    try:
        result = db.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": update_data}, return_document=True)
        
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    except Exception as e:
        print("Error al actualizar el usuario:", e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error al actualizar el usuario")
    
    return User(**result)


@router.delete("/delete/{id}",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    try:
        db.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"isRemove": True}})
        return {"message": "Usuario eliminado"}
    except Exception as e:
        print("Error al eliminar el usuario:", e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error al eliminar el usuario")

#Funciones para validar
def search_user(field: str, key):

    try:
        user = db.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}