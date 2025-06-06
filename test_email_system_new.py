#!/usr/bin/env python3
"""
Test Email System with New SMTP Credentials
This script tests if the email service works with the updated Gmail SMTP configuration
"""

from flask_backend.app.utils.emails import send_mail
from flask_backend.app.database.db import init_db
from flask import Flask
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


def test_email_system():
    """Test the email system with new SMTP credentials"""
    print_header("TESTING EMAIL SYSTEM")

    try:
        # Create Flask app context for environment variables
        app = Flask(__name__)
        init_db(app)

        with app.app_context():
            # Check environment variables
            email_user = os.environ.get('EMAIL_USER')
            email_pass = os.environ.get('EMAIL_PASS')

            print_info(f"Email User: {email_user}")
            print_info(
                f"Email Pass: {'*' * len(email_pass) if email_pass else 'Not Set'}")

            if not email_user or not email_pass:
                print_error(
                    "Email credentials not found in environment variables")
                return False

            # Test email sending
            test_recipient = "codexcoder082@gmail.com"  # Send to yourself for testing
            test_subject = "E-Commerce App - Email Test"
            test_body = """
            <html>
            <body>
                <h2>🎉 Email System Test Successful!</h2>
                <p>Your e-commerce application email system is now working correctly.</p>
                <p><strong>Test Details:</strong></p>
                <ul>
                    <li>SMTP Host: smtp.gmail.com</li>
                    <li>SMTP Port: 587</li>
                    <li>Security: TLS</li>
                    <li>From: {}</li>
                </ul>
                <p>You can now receive OTP emails for user registration and verification!</p>
                <br>
                <p><em>This is an automated test email from your e-commerce application.</em></p>
            </body>
            </html>
            """.format(email_user)

            print_info(f"Sending test email to: {test_recipient}")
            print_info("Please wait...")

            # Send test email
            success = send_mail(test_recipient, test_subject, test_body)

            if success:
                print_success("Email sent successfully! ✉️")
                print_success("Check your email inbox for the test message")
                print_info("Note: It may take a few minutes to arrive")
                return True
            else:
                print_error("Failed to send email")
                return False

    except Exception as e:
        print_error(f"Email test failed: {str(e)}")
        return False


def main():
    """Main function"""
    print_header("EMAIL SYSTEM VERIFICATION")

    success = test_email_system()

    if success:
        print_header("EMAIL SETUP COMPLETE")
        print_success("🎉 Email system is working correctly!")
        print_info("Your OTP emails will now be sent to users' email addresses")
        print_info("Next steps:")
        print_info("1. Test OTP registration with codexcoder082@gmail.com")
        print_info("2. Check your email for the OTP")
        print_info("3. Complete the verification process")
    else:
        print_header("EMAIL SETUP ISSUES")
        print_error("Email system needs attention")
        print_info("The app will still work with console OTPs for development")


if __name__ == "__main__":
    main()
