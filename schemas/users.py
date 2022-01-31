from pydantic import BaseModel
from pydantic.networks import EmailStr
import email_validator

from typing import Optional


class Users(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Profiles(BaseModel):
    user_id: int
    id_project: int
    user_type: str
    permissions: str

    class Config:
        orm_mode = True

# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserDelete(BaseModel):
    email: EmailStr



# Properties to receive via API on update
class UserUpdate(BaseModel):
    password: Optional[str] = None



  
