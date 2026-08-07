from datetime import datetime

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


                    post.youtube_video_id = result["id"]

                    post.status = "completed"


                else:

                    print(
                        f"Unsupported platform {post.platform}"
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
