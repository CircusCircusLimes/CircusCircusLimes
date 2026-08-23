import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import or_, and_

from forum.models import User, Message, db, error, valid_message

messages = Blueprint('messages', __name__)


@messages.app_context_processor
def inject_unread_message_count():
    """Makes the unread DM count available to every template (e.g. for a sidebar badge)."""
    if current_user.is_authenticated:
        count = Message.query.filter(
            Message.recipient_id == current_user.id,
            Message.is_read == False
        ).count()
        return {"unread_message_count": count}
    return {"unread_message_count": 0}


@messages.route('/messages')
@login_required
def inbox():
    thread_messages = Message.query.filter(
        or_(Message.sender_id == current_user.id, Message.recipient_id == current_user.id)
    ).order_by(Message.sentdate.desc()).all()

    conversations = {}
    for m in thread_messages:
        other = m.recipient if m.sender_id == current_user.id else m.sender
        if other.id not in conversations:
            conversations[other.id] = {
                "user": other,
                "last_message": m,
                "unread_count": Message.query.filter(
                    Message.sender_id == other.id,
                    Message.recipient_id == current_user.id,
                    Message.is_read == False
                ).count(),
            }

    conversation_list = sorted(
        conversations.values(),
        key=lambda c: c["last_message"].sentdate,
        reverse=True
    )

    return render_template("messages_inbox.html", conversations=conversation_list)


@messages.route('/messages/<username>')
@login_required
def conversation(username):
    other = User.query.filter(User.username == username).first()
    if not other:
        return error("That user does not exist!")
    if other.id == current_user.id:
        return error("You can't send messages to yourself!")

    thread = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.recipient_id == other.id),
            and_(Message.sender_id == other.id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.sentdate.asc()).all()

    # Mark any messages the other user sent us as read now that we're viewing the thread.
    unread = [m for m in thread if m.recipient_id == current_user.id and not m.is_read]
    if unread:
        for m in unread:
            m.is_read = True
        db.session.commit()

    return render_template("conversation.html", other=other, thread_messages=thread)


@messages.route('/action_send_message', methods=['POST'])
@login_required
def send_message():
    username = request.form.get('recipient', '').strip()
    content = request.form.get('content', '').strip()

    recipient = User.query.filter(User.username == username).first()
    if not recipient:
        flash("That user does not exist.", "error")
        return redirect(url_for('messages.inbox'))
    if recipient.id == current_user.id:
        flash("You can't send messages to yourself.", "error")
        return redirect(url_for('messages.inbox'))
    if not valid_message(content):
        flash("Message must be between 1 and 2000 characters.", "error")
        return redirect(url_for('messages.conversation', username=username))

    message = Message(content, datetime.datetime.now())
    message.sender = current_user
    message.recipient = recipient
    db.session.add(message)
    db.session.commit()

    return redirect(url_for('messages.conversation', username=username))
