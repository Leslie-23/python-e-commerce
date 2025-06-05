from app.database.db import db
from datetime import datetime


class Cart(db.Document):
    user = db.ReferenceField('User', required=True)
    items = db.ListField(db.DictField())
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'carts'
    }
