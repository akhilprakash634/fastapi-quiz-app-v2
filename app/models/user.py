from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    referral_code: Optional[str] = None
    age: int = Field(..., ge=0)

class UserInDB(UserCreate):
    hashed_password: str

class User(BaseModel):
    id: str
    name: str
    username: str
    email: EmailStr
    phone_number: Optional[str] = None
    age: int

class Token(BaseModel):
    access_token: str
    token_type: str