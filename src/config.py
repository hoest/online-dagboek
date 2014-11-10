# import os

SECRET_KEY = "<SECRET_KEY>"
DEBUG = True
# BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

SQLALCHEMY_DATABASE_URI = "postgresql://localhost/onlinedagboek"

CSRF_ENABLED = True

LOCALE = "nl_NL"

# UPLOAD_FOLDER = os.path.join(BASEDIR, "uploads")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

THUMBNAIL_WIDTH = 220
THUMBNAIL_HEIGHT = 220

FACEBOOK_APP_ID = "169415933126285"  # fake ID
FACEBOOK_APP_SECRET = None

MAIL_SERVER = "smtp.webfaction.com"
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = "Online Dagboek <noreply@online-dagboek.nl>"
MAIL_DEFAULT_BCC = "jelle@hoest.nl"
