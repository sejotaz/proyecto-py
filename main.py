from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from src.database import db


#Activar el entorno virtaul venv\Scripts\activate
#Encender el backend uvicorn main:app --reload
#Instalar todas las dependencias pip install -r requirements.txt
#DATABASE= mongodb+srv://Sejotaz:prueba123@mongodb1.ndvxls9.mongodb.net/
# 2:33:42



app = FastAPI()

# app.include_router(auth_router, prefix="/api", tags=["auth"])

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    name: str
    last_name: str
    username: str
    email: str
    password: str
    disabled: Optional[bool] = None

    class Config:
        populate_by_name = True

@app.get("/")
async def root():
    return {"message": "Arranco sho porque soy el local"}

@app.get("/users")
async def users():
    return User(name="ALejo", last_name="Ospina", username="Sejotaz", email="alejospina08@gmail.com", password="123", disabled=True)


