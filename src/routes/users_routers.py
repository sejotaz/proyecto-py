from fastapi import APIRouter, HTTPException, status
from src.models.UserModel import User
from src.schemas.user import user_schema
from database import db, client

router = APIRouter(prefix="/users", tags=["users"], responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}})


@router.get("/query")
async def users():
    return {"message": "Soy la ruta de usuarios"}

@router.get("/query/{id}")
async def users(id: int):
    return 'Soy la ruta de usuarios por ID '

@router.post("/create", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    id = db.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db.users.find_one({"_id": id}))

    return User(**new_user)