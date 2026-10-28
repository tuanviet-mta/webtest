from pydantic import BaseModel
from typing import List

class CartItem(BaseModel):
    product_id: int
    quantity: int
    price: int

class OrderRequest(BaseModel):
    customer_name: str
    customer_phone: str
    items: List[CartItem]