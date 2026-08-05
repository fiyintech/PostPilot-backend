from fastapi import APIRouter, UploadFile, File

from app.storage import upload_file


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_media(
    file: UploadFile = File(...)
):

    url = upload_file(
        file.file,
        file.filename
    )


    return {
        "url": url
    }
