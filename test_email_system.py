#!/usr/bin/env python3
"""
Test Email Configuration
This script tests if the SMTP email system is properly configured
"""

from flask_backend.app.utils.emails import send_mail
from flask_backend.app.database.db import init_db
from flask import Flask
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'flask_backend'))


def test_email_configuration():
    """Test if email sending is working"""
    print("="*50)
    print(" TESTING EMAIL CONFIGURATION")
    print("="*50)

    try:
        # Create Flask app and initialize database
        app = Flask(__name__)
        init_db(app)

        with app.app_context():
            # Test email sending
            test_email = "codexcoder082@gmail.com"
            subject = "🔐 Test Email from E-commerce App"
            body = """
            <html>
                <body>
                    <h2>Email Configuration Test</h2>
                    <p>✅ <strong>Success!</strong> Your email system is working properly.</p>
                    <p>This confirms that:</p>
                    <ul>
                        <li>SMTP configuration is correct</li>
                        <li>Gmail App Password is valid</li>
                        <li>Email delivery is functional</li>
                        <li>OTP emails will be sent successfully</li>
                    </ul>
                    <p>You can now test the complete OTP registration flow!</p>
                    <hr>
                    <p><small>Sent from your E-commerce Application</small></p>
                </body>
            </html>
            """

            print(f"📧 Attempting to send test email to: {test_email}")
            print("⏳ Please wait...")

            result = send_mail(test_email, subject, body)

            if result:
                print("✅ SUCCESS! Test email sent successfully!")
                print(f"📬 Check your inbox at {test_email}")
                print("📂 Also check your spam/junk folder")
                print("")
                print("🎉 Email system is working! OTP emails will be delivered.")
                print("")
                print("Next steps:")
                print("1. Check your email for the test message")
                print("2. Run the OTP registration test")
                print("3. You'll receive actual OTP emails!")

            else:
                print("❌ FAILED! Email could not be sent.")
                print("")
                print("Possible issues:")
                print("1. Check EMAIL_USER and EMAIL_PASS in .env file")
                print("2. Ensure Gmail App Password is correct")
                print("3. Check internet connection")
                print("4. Verify Gmail 2FA is enabled")

        return result

    except Exception as e:
        print(f"❌ Error testing email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    success = test_email_configuration()

    print("\n" + "="*50)
    if success:
        print("🎯 EMAIL SYSTEM READY FOR OTP DELIVERY!")
        print("   You can now register users and they'll receive OTP emails.")
    else:
        print("⚠️  EMAIL SYSTEM NEEDS CONFIGURATION")
        print("   OTPs will still appear in backend console as backup.")
    print("="*50)


if __name__ == "__main__":
    main()
