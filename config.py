"""
Flask configuration variables.
"""
from os import environ, path
from sqlalchemy import URL

basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

class Config:
    SECRET_KEY = 'kristofer'
    FLASK_APP = 'forum.app'

    # Reject request bodies over 2.5MB outright (avatar uploads are capped at
    # 2MB in forum/user.py; this is a blunt server-side backstop so an
    # oversized upload doesn't even get fully read into memory).
    MAX_CONTENT_LENGTH = int(2.5 * 1024 * 1024)

    DB_USER = environ.get("DB_USER")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_NAME = environ.get("DB_NAME", "circuscircuslimes")

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME
    )

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False