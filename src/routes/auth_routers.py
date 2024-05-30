from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone


app = FastAPI()

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET: "1234"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    name: str
    last_name: str
    username: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "Alejo": {
        "name": "Alejandro",
        "lastName": "Ospina",
        "username": "Sejotaz",
        "email": "alejospina08@gmail.com",
        "disabled": True,
        "password": "$2a$12$BVPMwV2Ukcsx5oy2JCgo.uV5jIxyNyvynNJFUtQzNS8nFWc.qYKAm"
    },
    "Jhony": {
        "name": "Jhony",
        "lastName": "Ospina",
        "username": "jhospina",
        "email": "jhospina@gmail.com",
        "disabled": True,
        "password": "$2a$12$xijXSQKoIStnm7Ce9YvU7eYZFo0ZD7v/9o5IAADf0Pcz85K1ZFJxu"
    }
}

# router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"message": "Not found"}})

async def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

# @router.get("/register")
# async def register():
#     return {"message": "Soy la ruta de registro"}

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta")
    

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub": user.username, "exp": expire}

    return {"acces_token": jwt.encode(access_token, SECRET ,algorithm=ALGORITHM), "token_type": "bearer"}
