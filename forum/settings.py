from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from forum.models import User, db
from forum.user import valid_username, valid_password, valid_email, username_taken, email_taken

settings = Blueprint('settings', __name__)


@settings.route('/settings')
@login_required
def settings_page():
    return render_template("settings.html")


@settings.route('/action_update_profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()

    errors = []

    if not valid_username(username):
        errors.append("Username must be 4-40 characters (letters, numbers, and !@#%& only).")
    elif username != current_user.username and username_taken(username):
        errors.append("That username is already taken.")

    if not valid_email(email):
        errors.append("Please enter a valid email address.")
    elif email != current_user.email and email_taken(email):
        errors.append("That email is already in use by another account.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for('settings.settings_page'))

    current_user.username = username
    current_user.email = email
    db.session.commit()
    flash("Your profile has been updated.", "success")
    return redirect(url_for('settings.settings_page'))


@settings.route('/action_change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    errors = []

    if not current_user.check_password(current_password):
        errors.append("Your current password is incorrect.")
    if not valid_password(new_password):
        errors.append("New password must be 6-40 characters (letters, numbers, and !@#%& only).")
    elif new_password != confirm_password:
        errors.append("New password and confirmation do not match.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for('settings.settings_page'))

    current_user.set_password(new_password)
    db.session.commit()
    flash("Your password has been changed.", "success")
    return redirect(url_for('settings.settings_page'))
