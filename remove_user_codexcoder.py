#!/usr/bin/env python3
"""
Remove specific user from MongoDB database
This script removes the user with email codexcoder082@gmail.com from the database
"""

import pymongo
from flask_backend.app.models.otp import OTP
from flask_backend.app.models.user import User
from flask_backend.app.database.db import get_database
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'flask_backend'))


def print_header(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")


def print_success(message):
    print(f"✅ {message}")


def print_error(message):
    print(f"❌ {message}")


def print_info(message):
    print(f"ℹ️  {message}")


def remove_user_and_related_data():
    """Remove user and all related data"""
    target_email = "codexcoder082@gmail.com"

    print_header("REMOVING USER FROM DATABASE")
    print_info(f"Target email: {target_email}")

    try:
        # Get database connection
        db = get_database()

        # First, check if user exists
        user_collection = db[User.COLLECTION_NAME]
        user = user_collection.find_one({"email": target_email})

        if not user:
            print_info(f"User with email {target_email} not found in database")
            return True

        user_id = user.get('_id')
        print_info(f"Found user with ID: {user_id}")
        print_info(f"User name: {user.get('name', 'N/A')}")
        print_info(f"Is verified: {user.get('is_verified', False)}")

        # Remove related OTP records
        otp_collection = db[OTP.COLLECTION_NAME]
        otp_result = otp_collection.delete_many({"user": user_id})
        print_info(f"Removed {otp_result.deleted_count} OTP records")

        # Remove user
        user_result = user_collection.delete_one({"_id": user_id})

        if user_result.deleted_count == 1:
            print_success(f"Successfully removed user: {target_email}")
            print_success("All related data cleaned up")
            return True
        else:
            print_error("Failed to remove user")
            return False

    except Exception as e:
        print_error(f"Error removing user: {str(e)}")
        return False


def verify_removal():
    """Verify that the user has been completely removed"""
    print_header("VERIFYING REMOVAL")
    target_email = "codexcoder082@gmail.com"

    try:
        db = get_database()

        # Check users collection
        user_collection = db[User.COLLECTION_NAME]
        user = user_collection.find_one({"email": target_email})

        if user:
            print_error(f"User still exists in database!")
            return False
        else:
            print_success(f"Confirmed: User {target_email} has been removed")

        # Check OTP collection
        otp_collection = db[OTP.COLLECTION_NAME]
        otp_count = otp_collection.count_documents({"email": target_email})

        if otp_count > 0:
            print_error(f"Found {otp_count} OTP records still in database!")
            return False
        else:
            print_success("Confirmed: No OTP records found for this email")

        return True

    except Exception as e:
        print_error(f"Error verifying removal: {str(e)}")
        return False


def main():
    """Main function"""
    print_header("USER REMOVAL TOOL")

    # Remove user and related data
    removal_success = remove_user_and_related_data()

    if removal_success:
        # Verify removal
        verification_success = verify_removal()

        if verification_success:
            print_header("REMOVAL COMPLETE")
            print_success("🎉 User and all related data successfully removed!")
            print_info("You can now test fresh OTP registration with:")
            print_info("Email: codexcoder082@gmail.com")
            print_info("The user can now register as if it's their first time")
        else:
            print_error("Removal verification failed")
    else:
        print_error("User removal failed")


if __name__ == "__main__":
    main()
