from fastapi import FastAPI
from routers import auth, expenses, incomes
from database import Base, engine
from routers import auth


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"Message": "Hello Welcome to the Personal Finance Manager go to http://localhost:8501/ for more info"}


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(incomes.router, prefix="/incomes", tags=["Incomes"])
