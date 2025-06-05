from app.database.db import db
from datetime import datetime


class Order(db.Document):
    user = db.ReferenceField('User', required=True)
    items = db.ListField(db.DictField())
    total_amount = db.FloatField(required=True)
    status = db.StringField(default='pending', choices=[
                            'pending', 'processing', 'shipped', 'delivered', 'cancelled'])
    payment_status = db.StringField(default='pending', choices=[
                                    'pending', 'completed', 'failed'])
    payment_method = db.StringField(required=True)
    shipping_address = db.ReferenceField('Address', required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'orders'
    }
