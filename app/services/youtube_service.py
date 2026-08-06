import os
import tempfile
import requests

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from app.database import SessionLocal
from app.models import YouTubeAccount



def get_youtube_client():

    db = SessionLocal()

    try:
        account = db.query(YouTubeAccount).first()

        if not account:
            raise Exception("No YouTube account connected")


        credentials = Credentials(
            token=account.access_token,
            refresh_token=account.refresh_token,
            token_uri=account.token_uri,
            client_id=account.client_id,
            client_secret=account.client_secret,
            scopes=account.scopes.split(" ")
        )


        youtube = build(
            "youtube",
            "v3",
            credentials=credentials
        )

        return youtube


    finally:
        db.close()



def download_video(url):

    response = requests.get(url)

    response.raise_for_status()


    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )


    temp.write(response.content)

    temp.close()


    return temp.name




def upload_video(
    file_path: str,
    title: str,
    description: str = "",
    privacy_status: str = "public"
):

    youtube = get_youtube_client()


    temporary_file = None


    try:

        # Download Supabase URL
        if file_path.startswith("http"):

            temporary_file = download_video(
                file_path
            )

            upload_path = temporary_file

        else:

            upload_path = file_path



        body = {

            "snippet": {

                "title": title,

                "description": description

            },

            "status": {

                "privacyStatus": privacy_status

            }

        }



        media = MediaFileUpload(
            upload_path,
            chunksize=-1,
            resumable=True
        )


        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )


        response = request.execute()


        return response



    finally:

        if temporary_file and os.path.exists(temporary_file):

            os.remove(temporary_file)
