from app.database.db import db


class Brand(db.Document):
    name = db.StringField(required=True, unique=True)
    description = db.StringField()

    meta = {
        'collection': 'brands'
    }
