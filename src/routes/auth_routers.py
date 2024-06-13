from fastapi import APIRouter, HTTPException, Depends, status, Form
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from src.models.UserModel import User
from database import db
from src.schemas.user import user_schema
from src.tools.funciones import search_user

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 10
SECRET = "1234"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"message": "Not found"}})

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas", headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception

    user = await db.users.find_one({"username": username})
    if user is None:
        raise exception

    return User(**user)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

def get_password_hash(password: str) -> str:
    return crypt.hash(password)

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    try:
        user_dict = user.model_dump()
        del user_dict["id"]

        hashed_password = get_password_hash(user_dict["password"])
        user_dict["password"] = hashed_password

        id = db.users.insert_one(user_dict).inserted_id

        new_user = user_schema(db.users.find_one({"_id": id}))

        return User(**new_user)
    except Exception as e:
        print("Error al crear el usuario:", e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Error al crear el usuario")

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = db.users.find_one({"username": form.username})
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user_dict = user_schema(user)
    if not crypt.verify(form.password, user_dict["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta")
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token_data = {
        "sub": user_dict["username"],
        "email": user_dict["email"],
        "role": user_dict["role"],
        "exp": expire
    }

    access_token = jwt.encode(access_token_data, SECRET, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
