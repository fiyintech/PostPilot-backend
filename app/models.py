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
