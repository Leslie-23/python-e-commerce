from app.database.db import db
from datetime import datetime


class Review(db.Document):
    user = db.ReferenceField('User', required=True)
    product = db.ReferenceField('Product', required=True)
    rating = db.IntField(required=True, min_value=1, max_value=5)
    comment = db.StringField()
    created_at = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'reviews'
    }
