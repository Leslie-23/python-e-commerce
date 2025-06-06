#!/usr/bin/env python3
from flask_backend.app.models.otp import OTP
from flask_backend.app.models.user import User
from flask_backend.app.database.db import init_db
from flask import Flask
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'flask_backend'))


def main():
    try:
        # Create Flask app and initialize database
        app = Flask(__name__)
        init_db(app)

        target_email = "codexcoder082@gmail.com"
        print(f"Looking for user with email: {target_email}")

        with app.app_context():
            # Check if user exists
            user = User.objects(email=target_email).first()

            if user:
                print(f"Found user: {user.name} - {user.email}")
                print(f"Is verified: {user.is_verified}")
                print(f"Is admin: {user.is_admin}")
                print(f"User ID: {user.id}")
                # Remove related OTP records
                otp_records = OTP.objects(email=target_email)
                otp_count = otp_records.count()
                if otp_count > 0:
                    otp_records.delete()
                    print(f"Removed {otp_count} OTP records")
                else:
                    print("No OTP records found for this user")

                # Remove user
                user.delete()
                print("✅ Successfully removed user")

            else:
                print("User codexcoder082@gmail.com not found in database")

            # Verify removal
            final_check = User.objects(email=target_email).first()
            if final_check:
                print("❌ User still exists!")
            else:
                print("✅ Confirmed: User has been completely removed")
                print("\n🎉 You can now test fresh OTP registration with:")
                print(f"   Email: {target_email}")
                print("   The user can register as if it's their first time")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
