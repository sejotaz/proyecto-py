from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class User(BaseModel):
    id: Optional[str] = None #UUID = Field(default_factory=uuid4) 
    name: str
    last_name: str
    username: str
    email: str
    password: str
    disabled: Optional[bool] = False
    role: str
    isRemove: Optional[bool] = False

class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    disabled: Optional[bool] = None
    role: Optional[str] = None
    isRemove: Optional[bool] = None
