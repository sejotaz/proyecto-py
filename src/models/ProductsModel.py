from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    id: Optional[str] = None 
    name_product: str
    price: float
    quantity: int
    buy: bool
    isAvaliable: bool
    isRemove: bool

class ProductUpdate(BaseModel):
    id: Optional[str] = None
    name_product: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    buy: Optional[bool] = None
    isAvaliable: Optional[bool] = None
    isRemove: Optional[bool] = None
