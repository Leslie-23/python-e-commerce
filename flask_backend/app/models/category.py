from app.database.db import db


class Category(db.Document):
    name = db.StringField(required=True, unique=True)
    description = db.StringField()

    meta = {
        'collection': 'categories'
    }
