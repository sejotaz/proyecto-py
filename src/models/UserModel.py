from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id") 
    name: str
    last_name: str
    username: str
    email: str
    password: str
    disabled: Optional[bool] = None
    role: str

    class Config:
        populate_by_name = True
