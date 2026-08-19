import datetime
from flask import Blueprint, request, redirect
from flask_login import current_user, login_required
from forum.models import Post, Comment, db, error

comments = Blueprint('comments', __name__)

@comments.route('/action_comment', methods=['POST'])
@login_required
def comment():

    post_id = int(request.args.get("post"))
    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        return error("That post does not exist!")

    content = request.form['content']
    postdate = datetime.datetime.now()
    comment = Comment(content, postdate)
    current_user.comments.append(comment)
    post.comments.append(comment)

    db.session.commit()

    return redirect("/viewpost?post=" + str(post_id))