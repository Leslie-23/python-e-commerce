#!/usr/bin/env python3
from flask_backend.app.models.otp import OTP
from flask_backend.app.models.user import User
from flask_backend.app.database.db import get_database
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'flask_backend'))


def main():
    try:
        db = get_database()
        print("Database connection successful")

        target_email = "codexcoder082@gmail.com"

        # Check if user exists
        user_collection = db[User.COLLECTION_NAME]
        user = user_collection.find_one({"email": target_email})

        if user:
            print(
                f"Found user: {user.get('name', 'N/A')} - {user.get('email')}")
            print(f"Is verified: {user.get('is_verified', False)}")
            print(f"User ID: {user.get('_id')}")

            # Remove OTP records first
            otp_collection = db[OTP.COLLECTION_NAME]
            otp_result = otp_collection.delete_many({"user": user.get('_id')})
            print(f"Removed {otp_result.deleted_count} OTP records")

            # Remove user
            user_result = user_collection.delete_one({"_id": user.get('_id')})
            if user_result.deleted_count == 1:
                print("✅ Successfully removed user")
            else:
                print("❌ Failed to remove user")

        else:
            print("User codexcoder082@gmail.com not found in database")

        # Verify removal
        final_check = user_collection.find_one({"email": target_email})
        if final_check:
            print("❌ User still exists!")
        else:
            print("✅ Confirmed: User has been removed")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
