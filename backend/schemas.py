from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


class IncomeCreate(BaseModel):
    user_id: int
    title: str
    amount: float
    description: str
    date: Optional[datetime] = None


class IncomeUpdate(BaseModel):
    title: Optional[str]
    amount: Optional[float]
    description: Optional[str]
    date: Optional[datetime]


class ExpenseCreate(BaseModel):
    user_id: int
    title: str
    amount: float
    category: str
    description: str
    date: Optional[datetime] = None


class ExpenseUpdate(BaseModel):
    title: str
    amount: Optional[float]
    category: Optional[str]
    description: Optional[str]
    date: Optional[datetime]
