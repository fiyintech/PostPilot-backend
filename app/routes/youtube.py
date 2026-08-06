from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from googleapiclient.discovery import build
from sqlalchemy.orm import Session

from app.auth.youtube import create_flow
from app.database import SessionLocal
from app.models import YouTubeAccount


router = APIRouter(
    prefix="/auth/youtube",
    tags=["YouTube"],
)


@router.get("/login")
def youtube_login(request: Request):

    flow = create_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    request.session["youtube_state"] = state
    request.session["youtube_code_verifier"] = flow.code_verifier

    return RedirectResponse(
        authorization_url
    )


@router.get("/callback")
def youtube_callback(
    request: Request,
    code: str | None = None
):

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing OAuth authorization code."
        )

    flow = create_flow()

    flow.code_verifier = request.session.get(
        "youtube_code_verifier"
    )

    if not flow.code_verifier:
        raise HTTPException(
            status_code=400,
            detail="Missing OAuth code verifier. Restart login."
        )

    flow.fetch_token(
        code=code
    )

    credentials = flow.credentials


    youtube = build(
        "youtube",
        "v3",
        credentials=credentials
    )


    channels = youtube.channels().list(
        part="snippet",
        mine=True
    ).execute()


    if not channels.get("items"):
        raise HTTPException(
            status_code=400,
            detail="No YouTube channel found."
        )


    channel = channels["items"][0]


    db: Session = SessionLocal()


    account = db.query(
        YouTubeAccount
    ).filter(
        YouTubeAccount.google_id == channel["id"]
    ).first()


    if account:

        account.access_token = credentials.token

        account.refresh_token = (
            credentials.refresh_token
            or account.refresh_token
        )

    else:

        account = YouTubeAccount(
            google_id=channel["id"],
            email="",
            channel_name=channel["snippet"]["title"],
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes=" ".join(credentials.scopes),
        )

        db.add(account)


    db.commit()
    db.close()


    return {
        "message": "YouTube account connected successfully!",
        "channel": channel["snippet"]["title"]
    }
