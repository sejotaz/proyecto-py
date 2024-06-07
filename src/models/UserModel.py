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
    name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    disabled: Optional[bool]
    role: Optional[str]
    isRemove: Optional[bool]
