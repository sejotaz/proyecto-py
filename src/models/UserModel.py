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
    disabled: Optional[bool] = None
    role: str

