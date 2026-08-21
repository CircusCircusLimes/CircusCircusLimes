
from flask import render_template, request, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
import datetime
from forum.models import User, Post, Comment, Subforum, Reaction, valid_content, valid_title, db, generateLinkPath, error
from forum.user import username_taken, email_taken, valid_username

posts = Blueprint('posts', __name__)


@posts.route('/addpost')
@login_required
def addpost():
    subforum_id = int(request.args.get("sub"))
    subforum = Subforum.query.filter(Subforum.id == subforum_id).first()
    if not subforum:
        return error("That subforum does not exist!")

    return render_template("createpost.html", subforum=subforum)


@posts.route('/viewpost')
def viewpost():
    postid = int(request.args.get("post"))
    post = Post.query.filter(Post.id == postid).first()

    if not post:
        return error("That post does not exist!")

    if not post.is_public and not current_user.is_authenticated:
        flash("This post is private. Log in to view it.", "error")
        return redirect(f"/subforum?sub={post.subforum_id}")

    subforumpath = post.subforum.path
    if not subforumpath:
        subforumpath = generateLinkPath(post.subforum.id)

    comments = Comment.query.filter(
        Comment.post_id == postid
    ).order_by(Comment.id.desc())

    like_count = Reaction.query.filter_by(
        post_id=postid,
        reaction_type="like"
    ).count()

    dislike_count = Reaction.query.filter_by(
        post_id=postid,
        reaction_type="dislike"
    ).count()

    heart_count = Reaction.query.filter_by(
        post_id=postid,
        reaction_type="heart"
    ).count()

    user_reaction = None

    if current_user.is_authenticated:
        reaction = Reaction.query.filter_by(
            post_id=postid,
            user_id=current_user.id
        ).first()

        if reaction:
            user_reaction = reaction.reaction_type

    return render_template(
        "viewpost.html",
        post=post,
        path=subforumpath,
        comments=comments,
        like_count=like_count,
        dislike_count=dislike_count,
        heart_count=heart_count,
        user_reaction=user_reaction
    )


@posts.route('/action_post', methods=['POST'])
@login_required
def action_post():
    subforum_id = int(request.args.get("sub"))
    subforum = Subforum.query.filter(Subforum.id == subforum_id).first()
    if not subforum:
        return redirect(url_for("subforums"))

    user = current_user
    title = request.form['title']
    content = request.form['content']
    is_public = request.form.get('is_public')  # added, MCC
    is_public = (is_public == 'on')  # added, MCC
    # check for valid posting
    errors = []
    retry = False
    if not valid_title(title):
        errors.append("Title must be between 4 and 140 characters long!")
        retry = True
    if not valid_content(content):
        errors.append("Post must be between 10 and 5000 characters long!")
        retry = True
    if retry:
        return render_template("createpost.html", subforum=subforum, errors=errors)
    post = Post(title, content, datetime.datetime.now(), is_public)  # added, MCC
    subforum.posts.append(post)
    user.posts.append(post)
    db.session.commit()
    return redirect("/viewpost?post=" + str(post.id))