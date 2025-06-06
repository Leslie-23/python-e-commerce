#!/usr/bin/env python3
"""
MongoDB Connection Test Script
Test your new MongoDB Atlas connection before updating the main application
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import sys


def test_mongodb_connection(uri):
    """Test MongoDB connection with the provided URI"""

    print("🔌 Testing MongoDB Connection...")
    print(f"📍 URI: {uri[:50]}...")  # Show only first part for security

    try:
        # Create MongoDB client
        client = MongoClient(uri)

        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")

        # List databases
        databases = client.list_database_names()
        print(f"📚 Available databases: {databases}")

        # Test creating a test collection
        test_db = client['test_connection']
        test_collection = test_db['test_data']

        # Insert a test document
        test_doc = {"test": "connection", "status": "working"}
        result = test_collection.insert_one(test_doc)
        print(f"📝 Test document inserted with ID: {result.inserted_id}")

        # Read the test document
        found_doc = test_collection.find_one({"test": "connection"})
        if found_doc:
            print("📖 Test document retrieved successfully!")

        # Clean up test data
        test_collection.delete_one({"_id": result.inserted_id})
        print("🧹 Test data cleaned up")

        # Close connection
        client.close()
        print("🔒 Connection closed")

        return True

    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False


def main():
    """Main function to test MongoDB connection"""

    print("🚀 MongoDB Connection Test Tool")
    print("=" * 50)

    # Option 1: Test with environment variable
    load_dotenv('flask_backend/.env')
    current_uri = os.getenv('MONGO_URI')

    if current_uri:
        print("\n1️⃣  Testing current .env configuration:")
        success = test_mongodb_connection(current_uri)
        if not success:
            print("❌ Current configuration failed")

    # Option 2: Test with manual input
    print("\n2️⃣  Enter your new MongoDB URI to test:")
    print("Format: mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority")

    new_uri = input("Enter new MongoDB URI (or press Enter to skip): ").strip()

    if new_uri:
        print("\n🧪 Testing your new MongoDB URI:")
        success = test_mongodb_connection(new_uri)

        if success:
            print("\n✅ Great! Your new MongoDB connection works!")
            update_choice = input(
                "Do you want to update your .env file with this URI? (y/n): ").lower()

            if update_choice == 'y':
                try:
                    # Read current .env file
                    env_path = 'flask_backend/.env'
                    with open(env_path, 'r') as f:
                        lines = f.readlines()

                    # Update MONGO_URI line
                    with open(env_path, 'w') as f:
                        for line in lines:
                            if line.startswith('MONGO_URI='):
                                f.write(f'MONGO_URI={new_uri}\n')
                            else:
                                f.write(line)

                    print(f"✅ Updated {env_path} with your new MongoDB URI!")
                    print("\n🔄 You should restart your Flask backend now.")

                except Exception as e:
                    print(f"❌ Failed to update .env file: {e}")
            else:
                print("ℹ️  You can manually update your .env file later.")
        else:
            print("❌ Please check your MongoDB URI and try again.")

    print("\n✨ Test completed!")


if __name__ == "__main__":
    main()
