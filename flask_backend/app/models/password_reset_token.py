from app.database.db import db
from datetime import datetime, timedelta


class PasswordResetToken(db.Document):
    email = db.EmailField(required=True)
    token = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    expires_at = db.DateTimeField(
        default=lambda: datetime.utcnow() + timedelta(hours=1))

    meta = {
        'collection': 'password_reset_tokens'
    }
