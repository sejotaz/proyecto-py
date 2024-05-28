from fastapi import FastAPI
from src.database import settings
from src.routes.auth import router as auth_router

#Activar el entorno virtaul venv\Scripts\activate
#Encender el backend uvicorn main:app --reload
#Instalar todas las dependencias pip install -r requirements.txt


app = FastAPI()

app.include_router(auth_router, prefix="/api", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the User API"}


