
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
    name: str
    username: str
    class Config():
        orm_mode = True

class UserAddress(BaseModel):
    user_id: int
    full_name: str
    mobile: str
    alternate_mobile: Optional[str] = None
    address_line1: str
    address_line2: Optional[str] = None
    landmark: Optional[str] = None
    city: str
    state: str
    pincode: str
    country: str
    class Config():
        orm_mode = True

class UserAddressResponse(UserAddress):
    id: int
    class Config():
        orm_mode = True