from pydantic import BaseModel
from typing import List, Optional

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float
    size: str
    color: str

class Order(BaseModel):
    user_id: int
    total_amount: float
    address_id: int
    payment_method: str
    items: List[OrderItem]
