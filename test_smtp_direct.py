#!/usr/bin/env python3
"""
Simple Email System Test
Tests the new SMTP credentials directly
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


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


def test_smtp_connection():
    """Test SMTP connection and email sending"""
    print_header("TESTING SMTP EMAIL SYSTEM")

    try:
        # Load environment variables from .env file
        env_path = os.path.join(os.path.dirname(
            __file__), 'flask_backend', '.env')
        load_dotenv(env_path)

        # Get email credentials
        email_user = os.environ.get('EMAIL_USER')
        email_pass = os.environ.get('EMAIL_PASS')
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))

        print_info(f"SMTP Host: {smtp_host}")
        print_info(f"SMTP Port: {smtp_port}")
        print_info(f"Email User: {email_user}")
        print_info(
            f"Email Pass: {'*' * len(email_pass) if email_pass else 'Not Set'}")

        if not email_user or not email_pass:
            print_error("Email credentials not found")
            return False

        # Create test email
        recipient = "codexcoder082@gmail.com"
        subject = "🎉 E-Commerce App - Email Test Success!"

        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4CAF50; text-align: center;">✅ Email System Working!</h2>
                
                <p>Great news! Your e-commerce application's email system is now properly configured and working.</p>
                
                <div style="background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2196F3;">Configuration Details:</h3>
                    <ul>
                        <li><strong>SMTP Host:</strong> {smtp_host}</li>
                        <li><strong>SMTP Port:</strong> {smtp_port}</li>
                        <li><strong>Security:</strong> TLS</li>
                        <li><strong>From Email:</strong> {email_user}</li>
                    </ul>
                </div>
                
                <p><strong>What this means:</strong></p>
                <ul>
                    <li>✅ OTP emails will now be sent to users' email addresses</li>
                    <li>✅ Registration verification emails will work</li>
                    <li>✅ Password reset emails will be delivered</li>
                </ul>
                
                <p style="margin-top: 30px; padding: 15px; background: #e8f5e8; border-radius: 5px;">
                    <strong>🎯 Next Step:</strong> Test the complete OTP flow by registering with your email!
                </p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 12px; color: #666; text-align: center;">
                    This is an automated test email from your e-commerce application.
                </p>
            </div>
        </body>
        </html>
        """

        # Create message
        message = MIMEMultipart()
        message['From'] = email_user
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))

        print_info(f"Sending test email to: {recipient}")
        print_info("Connecting to SMTP server...")

        # Connect and send email
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        print_info("TLS connection established")

        server.login(email_user, email_pass)
        print_info("SMTP authentication successful")

        server.send_message(message)
        server.quit()

        print_success("✉️ Email sent successfully!")
        print_success("Check your email inbox for the test message")
        print_info("Note: It may take a few seconds to a minute to arrive")

        return True

    except Exception as e:
        print_error(f"Email test failed: {str(e)}")
        return False


def main():
    """Main function"""
    success = test_smtp_connection()

    if success:
        print_header("EMAIL SETUP COMPLETE")
        print_success("🎉 Your email system is working perfectly!")
        print_info("Benefits:")
        print_info("• Users will receive OTP codes in their email")
        print_info("• Professional email delivery experience")
        print_info("• No need to check console logs for OTPs")
        print_info("")
        print_info("Ready to test the complete OTP flow!")
    else:
        print_header("EMAIL SETUP NEEDS ATTENTION")
        print_error("There was an issue with the email configuration")
        print_info("The app will still work with console OTPs as fallback")


if __name__ == "__main__":
    main()
