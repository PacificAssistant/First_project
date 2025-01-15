from app import db
from app.models import Posts


def delete_post_from_db(post_id):
    post = Posts.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return True
    return False
