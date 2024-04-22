from pydantic import BaseModel
from typing import List, Optional

class Cart(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    size: str
    color: str
    is_gift: Optional[bool] = False

    class Config():
        orm_mode = True
