from flask import Blueprint, request, redirect
from flask_login import login_required, current_user
from forum.models import db, Comment, CommentReaction, error

comment_reactions = Blueprint("comment_reactions", __name__)

@comment_reactions.route("/action_comment_reaction", methods=["POST"])
@login_required
def react_to_comment():

    comment_id = request.form.get("comment_id")

    reaction_type = request.form.get("reaction_type")

    if reaction_type not in ["like", "dislike", "heart"]:
        return error("Invalid reaction.")

    comment = Comment.query.filter(Comment.id == comment_id).first()

    if not comment:
        return error("That comment does not exist.")

    existing_reaction = CommentReaction.query.filter_by(
        user_id=current_user.id,
        comment_id=comment.id
    ).first()

    if existing_reaction:

        if existing_reaction.reaction_type == reaction_type:
            db.session.delete(existing_reaction)

        else:
            existing_reaction.reaction_type = reaction_type

    else:

        reaction = CommentReaction(reaction_type)
        reaction.user_id = current_user.id
        reaction.comment_id = comment.id
        db.session.add(reaction)

    db.session.commit()

    return redirect("/viewpost?post=" + str(comment.post_id))