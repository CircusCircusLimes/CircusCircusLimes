import datetime
from flask import Blueprint, request, redirect, flash
from flask_login import current_user, login_required
from forum.models import Post, Comment, db, error, valid_comment

comments = Blueprint('comments', __name__)

@comments.route('/action_comment', methods=['POST'])
@login_required
def comment():
    post_value = request.args.get("post")

    if not post_value:
        flash("A post ID is required.", "error")
        return redirect("/")

    try:
        post_id = int(post_value)
    except ValueError:
        flash("Invalid post ID.", "error")
        return redirect("/")

    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        flash("That post does not exist.", "error")
        return redirect("/")

    content = request.form.get("content", "").strip()

    if not valid_comment(content):
        flash("Comment must be between 1 and 1000 characters.", "error")
        return redirect("/viewpost?post=" + str(post_id))

    postdate = datetime.datetime.now()
    comment = Comment(content, postdate)

    current_user.comments.append(comment)
    post.comments.append(comment)

    db.session.commit()

    return redirect("/viewpost?post=" + str(post_id))