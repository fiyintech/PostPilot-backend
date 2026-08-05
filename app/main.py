from fastapi import FastAPI

from app.database import engine, Base
from app.models import ScheduledPost

from app.routes import posts
from app.routes import upload

Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="PostPilot API"
)


app.include_router(
    posts.router
)

app.include_router(
    upload.router
)

@app.get("/")
def home():

    return {
        "message": "PostPilot is running 🚀"
    }
