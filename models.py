from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from pygments.util import looks_like_xml

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    twofa_secret = db.Column(db.String(64))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    is_premium = db.Column(db.Boolean, default=False)

    stripe_customer_id = db.Column(db.String(255))

class LoginLog(db.Model):

    __tablename__ = "login_logs"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80))

    ip_address = db.Column(db.String(100))

    user_agent = db.Column(db.String(255))

    successful = db.Column(db.Boolean)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    print("lol")