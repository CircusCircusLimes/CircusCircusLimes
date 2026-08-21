
from .models import User
import re

##
# Some utility routines.
##

password_regex = re.compile("^[a-zA-Z0-9!@#%&]{6,40}$")
username_regex = re.compile("^[a-zA-Z0-9!@#%&]{4,40}$")
email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
#Account checks
def valid_username(username):
	if not username_regex.match(username):
		#username does not meet password reqirements
		return False
	#username is not taken and does meet the password requirements
	return True
def valid_password(password):
	return password_regex.match(password)

def username_taken(username):
	return User.query.filter(User.username == username).first()
def email_taken(email):
	return User.query.filter(User.email == email).first()

def valid_email(email):
	return bool(email_regex.match(email))

# Avatar upload checks
ALLOWED_AVATAR_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_AVATAR_BYTES = 2 * 1024 * 1024  # 2MB

def valid_avatar_filename(filename):
	if not filename or "." not in filename:
		return False
	ext = filename.rsplit(".", 1)[1].lower()
	return ext in ALLOWED_AVATAR_EXTENSIONS

def avatar_extension(filename):
	return filename.rsplit(".", 1)[1].lower()
