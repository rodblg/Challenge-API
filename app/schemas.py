from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    balance: Optional[float] = 0.0

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    value: float
    name_movement: str

    class Config:
        orm_mode = True


class UserReturn(BaseModel):
    name: str
    email: EmailStr
    balance: float
    created_at: datetime
    class Config:
        orm_mode = True

class TransactionReturn(BaseModel):
    id: int
    value: float
    name_movement: str
    created_at: datetime
    class Config:
        orm_mode = True


class Token(BaseModel):
    
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class UserLogin(BaseModel):
    email: EmailStr
    password: str