import os

from dotenv import load_dotenv
from supabase import create_client


load_dotenv()


supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)


def upload_file(
    file,
    filename
):

    content = file.read()


    response = supabase.storage.from_(
        "postpilot-media"
    ).upload(
        filename,
        content
    )


    url = supabase.storage.from_(
        "postpilot-media"
    ).get_public_url(
        filename
    )


    return url
