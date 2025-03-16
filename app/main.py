import asyncio

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.connect import session_manager
from app.src.database.db import db
from app.src.routes import books, comments, auth

app = FastAPI()


app.include_router(auth.router, prefix="/api")
app.include_router(books.router, prefix="/products")
app.include_router(comments.router, prefix="/comments")


async def check_database_health():
    while True:
        async with session_manager.session() as session:
            try:
                await healthchecker(session)
                print("Healthcheck passed!")
            except Exception as e:
                print(f"Healthcheck failed: {e}")
        await asyncio.sleep(600)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(check_database_health())


@app.get("/")
async def root():
    return {"message": "Welcome to 'Eniki-Beniki' bookshop for kids."}


@app.get("/api/healthchecker")
async def healthchecker(session: AsyncSession = Depends(db)):
    try:
        result = await session.execute(text("SELECT 1"))
        result = result.fetchone()
        if not result:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to 'Eniki-Beniki' bookshop for kids."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
