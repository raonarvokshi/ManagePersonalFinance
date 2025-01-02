from models import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Income, User
from schemas import IncomeCreate, IncomeUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_income(income: IncomeCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == income.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_income = Income(user_id=income.user_id, **
                       income.dict(exclude={"user_id"}))
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


@router.get("/")
def read_incomes(user_id: int, db: Session = Depends(get_db)):
    return db.query(Income).filter(Income.user_id == user_id).all()


@router.put("/{income_id}")
def update_income(income_id: int, income: IncomeUpdate, db: Session = Depends(get_db)):
    db_income = db.query(Income).filter(Income.id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found!")

    for key, value in income.dict(exclude_unset=True).items():
        setattr(db_income, key, value)

    db.commit()
    db.refresh(db_income)
    return db_income


@router.delete("/{income_id}")
def delete_income(income_id: int, db: Session = Depends(get_db)):
    db_income = db.query(Income).filter(Income.id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    db.delete(db_income)
    db.commit()
    return {"message": "Income deleted successfully"}
