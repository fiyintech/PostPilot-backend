from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from pydantic import BaseModel

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






class UpdatePostRequest(BaseModel):

    caption: str

    scheduled_time: str

    platform: str






@router.post("/create")
async def create_scheduled_post(

    file: UploadFile = File(...),

    caption: str = Form(...),

    platform: str = Form(...),

    scheduled_time: str = Form(...),

    db: Session = Depends(get_db)

):


    filename = (

        str(uuid.uuid4())

        + "_"

        + file.filename

    )



    media_url = upload_file(

        file.file,

        filename

    )



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


    return db.query(
        ScheduledPost
    ).all()







@router.put("/{post_id}")
def update_post(

    post_id: int,

    data: UpdatePostRequest,

    db: Session = Depends(get_db)

):


    post = db.query(
        ScheduledPost
    ).filter(
        ScheduledPost.id == post_id
    ).first()



    if not post:

        raise HTTPException(

            status_code=404,

            detail="Post not found"

        )



    if post.status != "pending":

        raise HTTPException(

            status_code=400,

            detail="Only pending posts can be edited"

        )



    post.caption = data.caption


    post.platform = data.platform


    post.scheduled_time = datetime.fromisoformat(

        data.scheduled_time

    )



    db.commit()

    db.refresh(post)



    return post







@router.delete("/{post_id}")
def delete_post(

    post_id: int,

    db: Session = Depends(get_db)

):


    post = db.query(
        ScheduledPost
    ).filter(
        ScheduledPost.id == post_id
    ).first()



    if not post:

        raise HTTPException(

            status_code=404,

            detail="Post not found"

        )



    if post.status != "pending":

        raise HTTPException(

            status_code=400,

            detail="Only pending posts can be deleted"

        )



    db.delete(post)

    db.commit()



    return {

        "message":
        "Post deleted successfully"

    }
