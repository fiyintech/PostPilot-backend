from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database import SessionLocal
from app.models import ScheduledPost
from app.storage import upload_file


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@router.post("/create")
async def create_scheduled_post(
    file: UploadFile = File(...),
    caption: str = Form(...),
    platform: str = Form(...),
    scheduled_time: str = Form(...),
    db: Session = Depends(get_db)
):

    # Create unique filename

    filename = (
        str(uuid.uuid4())
        + "_"
        + file.filename
    )


    # Upload media

    media_url = upload_file(
        file.file,
        filename
    )


    # Create database record

    post = ScheduledPost(
        media_url=media_url,
        caption=caption,
        platform=platform,
        scheduled_time=datetime.fromisoformat(
            scheduled_time
        ),
        status="pending"
    )


    db.add(post)

    db.commit()

    db.refresh(post)


    return post



@router.get("/")
def get_posts(
    db: Session = Depends(get_db)
):

    posts = db.query(
        ScheduledPost
    ).all()


    return posts
