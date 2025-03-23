import asyncio
import httpx

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.database.connect import session_manager
from app.src.database.db import db
from app.src.routes import books, review, auth

app = FastAPI()

origins = ["http://localhost:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api")
app.include_router(books.router, prefix="/products")
app.include_router(review.router, prefix="/reviews")


async def check_database_health():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                url = "https://bookshop-backend-dnzd.onrender.com"
                response = await client.get(url)
                print(f"Keep Alive Status: {response.status_code}")
            except Exception as e:
                print(f"Keep Alive Failed: {e}")
            await asyncio.sleep(300)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(check_database_health())


@app.get("/")
async def root():
    return {"message": "Welcome to 'Eniki-Beniki' bookshop for kids."}


@app.head("/")
async def head_root():
    return {}


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
