from typing import Dict, Optional
from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: Optional[str] = None
    name_product: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    buy: Optional[bool] = None
    isAvaliable: Optional[bool] = None
    isRemove: Optional[bool] = None