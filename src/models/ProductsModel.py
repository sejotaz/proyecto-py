from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    id: Optional[str] = None 
    name_product: str
    price: float
    img: str
    quantity: int
    buy: Optional[bool] = False
    isAvaliable: Optional[bool] = False
    isRemove: Optional[bool] = False

class ProductUpdate(BaseModel):
    id: Optional[str] = None
    name_product: Optional[str] = None
    price: Optional[float] = None
    img: Optional[str] = None
    quantity: Optional[int] = None
    buy: Optional[bool] = None
    isAvaliable: Optional[bool] = None
    isRemove: Optional[bool] = None
