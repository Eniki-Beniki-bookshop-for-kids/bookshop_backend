from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import db
from src.routes import books

app = FastAPI()


app.include_router(books.router, prefix="/products")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
async def healthchecker(session: AsyncSession = Depends(db)):
    try:
        result = await session.execute(text("SELECT 1"))
        result = result.fetchone()
        if not result:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
