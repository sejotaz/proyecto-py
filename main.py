from fastapi import FastAPI
from src.database import db
from src.routes import users_routers, auth_routers


#Activar el entorno virtaul venv\Scripts\activate
#Encender el backend uvicorn main:app --reload
#Instalar todas las dependencias pip install -r requirements.txt
#DATABASE= mongodb+srv://Sejotaz:prueba123@mongodb1.ndvxls9.mongodb.net/
# 2:33:42

app = FastAPI()

# Routers
app.include_router(users_routers.router)
app.include_router(auth_routers.router)

@app.get("/")
async def root():
    return {"message": "Arranco sho porque soy el local"}




