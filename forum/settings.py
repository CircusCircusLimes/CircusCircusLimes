from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from forum.models import db
from forum.user import valid_password

settings = Blueprint('settings', __name__)


@settings.route('/settings')
@login_required
def settings_page():
    return render_template("settings.html")


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
