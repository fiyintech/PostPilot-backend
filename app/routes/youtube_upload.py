from fastapi import APIRouter, HTTPException

from app.services.youtube_service import upload_video


router = APIRouter(
    prefix="/youtube",
    tags=["YouTube Upload"]
)


@router.post("/upload")
def youtube_upload(
    file_path: str,
    title: str,
    description: str = ""
):

    try:

        result = upload_video(
            file_path=file_path,
            title=title,
            description=description
        )

        return {
            "message": "Video uploaded successfully",
            "video_id": result["id"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
