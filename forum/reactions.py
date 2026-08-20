from flask import Blueprint, request, redirect
from flask_login import login_required, current_user
from forum.models import db, Post, Reaction, error

reactions = Blueprint("reactions", __name__)

@reactions.route("/action_reaction", methods=["POST"])
@login_required
def react():
    post_id = request.form.get("post_id")
    reaction_type = request.form.get("reaction_type")

    if reaction_type not in ["like", "dislike", "heart"]:
        return error("Invalid reaction.")

    post = Post.query.filter(Post.id == post_id).first()

    if not post:
        return error("That post does not exist.")

    existing_reaction = Reaction.query.filter_by(
        user_id=current_user.id,
        post_id=post.id
    ).first()

    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            db.session.delete(existing_reaction)
        else:
            existing_reaction.reaction_type = reaction_type
    else:
        reaction = Reaction(reaction_type)
        reaction.user = current_user
        reaction.post = post
        db.session.add(reaction)

    db.session.commit()

    return redirect("/viewpost?post=" + str(post.id))