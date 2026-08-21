import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from forum.models import db
from forum.user import (
    valid_username, valid_email, username_taken, email_taken,
    valid_avatar_filename, avatar_extension, MAX_AVATAR_BYTES,
)

profile = Blueprint('profile', __name__)

AVATAR_SUBDIR = os.path.join('images', 'avatars')


def _avatar_dir():
    path = os.path.join(current_app.root_path, 'static', AVATAR_SUBDIR)
    os.makedirs(path, exist_ok=True)
    return path


@profile.route('/profile')
@login_required
def profile_page():
    return render_template("profile.html")


@profile.route('/action_update_username', methods=['POST'])
@login_required
def update_username():
    username = request.form.get('username', '').strip()

    if not valid_username(username):
        flash("Username must be 4-40 characters (letters, numbers, and !@#%& only).", "error")
    elif username != current_user.username and username_taken(username):
        flash("That username is already taken.", "error")
    else:
        current_user.username = username
        db.session.commit()
        flash("Your username has been updated.", "success")

    return redirect(url_for('profile.profile_page'))


@profile.route('/action_update_email', methods=['POST'])
@login_required
def update_email():
    email = request.form.get('email', '').strip()

    if not valid_email(email):
        flash("Please enter a valid email address.", "error")
    elif email != current_user.email and email_taken(email):
        flash("That email is already in use by another account.", "error")
    else:
        current_user.email = email
        db.session.commit()
        flash("Your email has been updated.", "success")

    return redirect(url_for('profile.profile_page'))


@profile.route('/action_update_avatar', methods=['POST'])
@login_required
def update_avatar():
    upload = request.files.get('avatar')

    if upload is None or upload.filename == '':
        flash("Please choose an image to upload.", "error")
        return redirect(url_for('profile.profile_page'))

    filename = secure_filename(upload.filename)

    if not valid_avatar_filename(filename):
        flash("Profile pictures must be a PNG, JPG, GIF, or WEBP file.", "error")
        return redirect(url_for('profile.profile_page'))

    # Peek at the size without trusting Content-Length: seek to the end of
    # the stream, read the position, then rewind before saving.
    upload.stream.seek(0, os.SEEK_END)
    size = upload.stream.tell()
    upload.stream.seek(0)

    if size > MAX_AVATAR_BYTES:
        flash("Profile pictures must be 2MB or smaller.", "error")
        return redirect(url_for('profile.profile_page'))

    new_filename = f"user_{current_user.id}_{uuid.uuid4().hex}.{avatar_extension(filename)}"
    avatar_dir = _avatar_dir()
    upload.save(os.path.join(avatar_dir, new_filename))

    old_filename = current_user.avatar_filename
    current_user.avatar_filename = new_filename
    db.session.commit()

    if old_filename:
        old_path = os.path.join(avatar_dir, old_filename)
        if os.path.exists(old_path):
            os.remove(old_path)

    flash("Your profile picture has been updated.", "success")
    return redirect(url_for('profile.profile_page'))
