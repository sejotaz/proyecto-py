from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone




ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 2
SECRET = "1234"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"message": "Not found"}})

class User(BaseModel):
    name: str
    last_Name: str
    username: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "Sejotaz": {
        "name": "Alejandro",
        "last_Name": "Ospina",
        "username": "Sejotaz",
        "email": "alejospina08@gmail.com",
        "disabled": False,
        "password": "$2a$12$BVPMwV2Ukcsx5oy2JCgo.uV5jIxyNyvynNJFUtQzNS8nFWc.qYKAm"
    },
    "Jhony": {
        "name": "Jhony",
        "last_Name": "Ospina",
        "username": "jhospina",
        "email": "jhospina@gmail.com",
        "disabled": False,
        "password": "$2a$12$xijXSQKoIStnm7Ce9YvU7eYZFo0ZD7v/9o5IAADf0Pcz85K1ZFJxu"
    }
}


async def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
async def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
        exception =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas", headers={"WWW-Authenticate": "Bearer"})
        try:
            username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
            if username is None:
                raise exception
        except JWTError:
            raise exception
        
        user = await search_user(username)
        if user is None:
            raise exception

        return user


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

# @router.get("/register")
# async def register():
#     return {"message": "Soy la ruta de registro"}

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = await search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta")
    

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub": user.username, "exp": expire}

    return {"acces_token": jwt.encode(access_token, SECRET ,algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
