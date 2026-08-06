from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from apscheduler.schedulers.background import BackgroundScheduler

from app.scheduler import process_scheduled_posts
from app.database import engine, Base

from app.routes import youtube
from app.routes import posts
from app.routes import upload
from app.routes import youtube_upload


# Create database tables

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="PostPilot API",
    version="1.0.0"
)


# Allow frontend access

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://postpilot-wine-nine.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Session middleware for OAuth

app.add_middleware(
    SessionMiddleware,
    secret_key="postpilot-secret-key-change-this"
)


# Include routes

app.include_router(youtube.router)
app.include_router(posts.router)
app.include_router(upload.router)
app.include_router(youtube_upload.router)



# Scheduler

scheduler = BackgroundScheduler()


@app.on_event("startup")
def startup_event():

    scheduler.add_job(
        process_scheduled_posts,
        "interval",
        seconds=30,
        id="scheduled_posts_worker",
        replace_existing=True,
    )

    scheduler.start()

    print("PostPilot scheduler started")



@app.on_event("shutdown")
def shutdown_event():

    scheduler.shutdown()

    print("PostPilot scheduler stopped")



@app.get("/")
def root():

    return {
        "message": "PostPilot backend running"
    }
