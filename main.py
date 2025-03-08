from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.routes import books

app = FastAPI()


app.include_router(books.router, prefix="/goods")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
async def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if not result:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
