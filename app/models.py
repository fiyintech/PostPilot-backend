from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base


class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    media_url = Column(
        String,
        nullable=False
    )

    caption = Column(
        Text,
        nullable=False
    )

    platform = Column(
        String,
        nullable=False
    )

    scheduled_time = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        String,
        default="pending"
    )

    youtube_video_id = Column(
        String,
        nullable=True
    )


class YouTubeAccount(Base):
    __tablename__ = "youtube_accounts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    google_id = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    channel_name = Column(
        String
    )

    access_token = Column(
        Text,
        nullable=False
    )

    refresh_token = Column(
        Text,
        nullable=False
    )

    token_uri = Column(
        String
    )

    client_id = Column(
        String
    )

    client_secret = Column(
        String
    )

    scopes = Column(
        Text
    )
