from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"message": "Not Found"}})


@router.get("/create")
async def users():
    return {"message": "Soy la ruta de usuarios"}