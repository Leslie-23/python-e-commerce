from app.database.db import db


class Address(db.Document):
    user = db.ReferenceField('User', required=True)
    name = db.StringField(required=True)
    street = db.StringField(required=True)
    city = db.StringField(required=True)
    state = db.StringField(required=True)
    pin_code = db.StringField(required=True)
    phone = db.StringField(required=True)

    meta = {
        'collection': 'addresses'
    }
