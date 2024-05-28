from fastapi import APIRouter, HTTPException
from src.models.UserModel import User 
from src.services.auth_controller import AuthController
import logging


router = APIRouter()

@router.post("/register", response_model=User)
def create_user(user: User):
    try:
        logging.info(create_user())
        return AuthController.create_user(user)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
