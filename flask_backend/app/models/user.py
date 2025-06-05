from app.database.db import db


class User(db.Document):
    name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    is_verified = db.BooleanField(default=False)
    is_admin = db.BooleanField(default=False)

    meta = {
        'collection': 'users'
    }
