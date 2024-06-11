from fastapi import FastAPI
from database import db
from src.routes import users_routers, auth_routers, products_routers

#Crear un entorno virtual python -m venv venv
#Activar el entorno virtaul venv\Scripts\activate
#Encender el backend uvicorn main:app --reload
#Instalar todas las dependencias pip install -r requirements.txt
#DATABASE= mongodb+srv://Sejotaz:prueba123@mongodb1.ndvxls9.mongodb.net/
# 6:30:10
# Generar un token random openssl rand -hex 32

app = FastAPI()

# Routers
app.include_router(users_routers.router)
app.include_router(auth_routers.router)
app.include_router(products_routers.router)

@app.get("/")
async def root():
    return {"message": "Arranco sho porque soy el local"}




