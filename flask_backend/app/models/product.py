from app.database.db import db


class Product(db.Document):
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    price = db.FloatField(required=True)
    discounted_price = db.FloatField()
    image_url = db.StringField()
    brand = db.ReferenceField('Brand')
    category = db.ReferenceField('Category')
    stock = db.IntField(required=True, default=0)
    rating = db.FloatField(default=0)
    num_reviews = db.IntField(default=0)

    meta = {
        'collection': 'products'
    }
