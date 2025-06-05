import os
from flask_mongoengine import MongoEngine

db = MongoEngine()


def init_db(app):
    app.config['MONGODB_SETTINGS'] = {
        'host': os.environ.get('MONGO_URI', 'mongodb://localhost:27017/ecommerce')
    }
    db.init_app(app)
    print('Connected to DB')
