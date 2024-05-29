from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"message": "Not found"}})

@router.get("/register")
async def register():
    return {"message": "Soy la ruta de registro"}

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    return {"message": "Soy la ruta de registro"}
