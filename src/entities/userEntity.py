from typing import Dict, Optional
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: str
    name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None
    role: Optional[str] = None
    isRemove: Optional[bool] = None