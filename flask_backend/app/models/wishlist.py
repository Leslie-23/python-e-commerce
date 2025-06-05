from app.database.db import db


class Wishlist(db.Document):
    user = db.ReferenceField('User', required=True)
    products = db.ListField(db.ReferenceField('Product'))

    meta = {
        'collection': 'wishlists'
    }
