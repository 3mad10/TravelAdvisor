import schemas
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import itinerary, login, user

from core.config import settings
import uvicorn
from sqlmodel import Session


app = FastAPI()

app.include_router(itinerary.router)
app.include_router(login.router)
app.include_router(user.router)

# TODO add extra origins and move to settings
app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def main():
    return "Travel"

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)