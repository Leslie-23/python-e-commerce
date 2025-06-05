import os
from flask_mongoengine import MongoEngine

db = MongoEngine()


def init_db(app):
    mongo_uri = os.environ.get(
        'MONGO_URI', 'mongodb://localhost:27017/ecommerce')

    # Configure MongoDB connection
    app.config['MONGODB_SETTINGS'] = {
        'host': mongo_uri
    }

    # Check if we're using MongoDB Atlas
    is_atlas = "mongodb+srv://" in mongo_uri

    # Initialize the database connection
    try:
        db.init_app(app)
        if is_atlas:
            print('Connected to MongoDB Atlas')
        else:
            print('Connected to local MongoDB')
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        if not is_atlas:
            print("MongoDB is not running locally. You have two options:")
            print("1. Install and start MongoDB locally")
            print("2. Use MongoDB Atlas by updating the MONGO_URI in your .env file")
            print("To use MongoDB Atlas, sign up at https://www.mongodb.com/cloud/atlas")
            print("and update your .env file with the connection string")
        else:
            print(
                "Please make sure your MongoDB Atlas connection string is correct in the .env file")
            print(
                "and that you've set up network access to allow connections from your IP address")
