from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app.models import ScheduledPost
from app.services.youtube_service import upload_video


def process_scheduled_posts():
    db = SessionLocal()

    try:
        posts = (
            db.query(ScheduledPost)
            .filter(
                ScheduledPost.status == "pending",
                ScheduledPost.scheduled_time <= datetime.now()
            )
            .all()
        )

        for post in posts:
            print(f"Processing post {post.id}")

            try:
                if post.platform == "YouTube":

                    result = upload_video(
                        file_path=post.media_url,
                        title=post.caption,
                        description=post.caption
                    )

                    print(
                        f"YouTube upload completed: {result}"
                    )

                    # Save only the YouTube video ID
                    post.youtube_video_id = result["id"]

                    post.status = "completed"

                else:
                    print(
                        f"Platform {post.platform} not supported yet"
                    )

                    post.status = "failed"

                db.commit()

            except Exception as e:
                db.rollback()

                post.status = "failed"

                db.commit()

                print(
                    f"Post {post.id} failed: {e}"
                )

    finally:
        db.close()


scheduler = BackgroundScheduler()

scheduler.add_job(
    process_scheduled_posts,
    "interval",
    seconds=30
)


def start_scheduler():
    scheduler.start()
