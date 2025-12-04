import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # --- Flask & SQLAlchemy ---
    SECRET_KEY = os.environ.get("SECRET_KEY") or \
        "e44bb6d0a3e41a1c9e0d9bfb7acb4f19c7f1de2b9f95811a3cd5329bd2ee58f3"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(BASE_DIR, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Session / Cookie Settings ---
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Change to True when using HTTPS in production
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # --- Email Configuration ---
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")
