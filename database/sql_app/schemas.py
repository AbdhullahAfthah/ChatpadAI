from pydantic import BaseModel
from typing import List


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    username: str or None = None




class ResourceBase(BaseModel):
    pdf: str
    url: str


class ResourceCreate(ResourceBase):
    pass


class Resource(ResourceBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):
    email: str
    username: str

# UserInDB == UserCreate
class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int
    is_active: bool
    resources: List[Resource] = []

    class Config:
        orm_mode = True





class AdminBase(BaseModel):
    username: str


class AdminCreate(AdminBase):
    password: str


class Admin(AdminBase):
    id: int
    is_admin: bool
    users: List[User] = []
    resources: List[Resource] = []

    class Config:
        orm_mode = True


class URLData(BaseModel):
    url: str