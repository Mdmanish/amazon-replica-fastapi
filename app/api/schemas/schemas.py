
from pydantic import BaseModel
from typing import List, Optional

class RegisterUser(BaseModel):
    name: str
    username: str
    password: str
    confirm_password: str

class LoginUser(BaseModel):
    username: str
    password: str



class ResponseUser(BaseModel):
    id: int
    name: str
    mobile: str
    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None



class ProductWithImage(BaseModel):
    id: int
    name: str
    description: str
    price: float
    discount: float
    url: str

    class Config():
        orm_mode = True
