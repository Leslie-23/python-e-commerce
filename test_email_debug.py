#!/usr/bin/env python3
"""
Debug Email System - Test SMTP Connection and Email Sending
"""

import json
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
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


def test_smtp_connection():
    """Test direct SMTP connection"""
    print_header("TESTING SMTP CONNECTION")

    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    email_user = 'codexcoder082@gmail.com'
    email_pass = 'ngxblhhvslnvcflr'

    print_info(f"SMTP Host: {smtp_host}")
    print_info(f"SMTP Port: {smtp_port}")
    print_info(f"Email User: {email_user}")

    try:
        # Create SMTP connection
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Enable TLS

        print_success("SMTP connection established")

        # Login
        server.login(email_user, email_pass)
        print_success("SMTP login successful")

        # Send test email
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = 'marvelmmk2005@gmail.com'
        msg['Subject'] = 'Test Email - OTP System Debug'

        body = """
        This is a test email to verify SMTP configuration.
        
        If you receive this email, the SMTP system is working correctly.
        
        Test OTP: 1234
        
        Sent from E-commerce OTP System
        """

        msg.attach(MIMEText(body, 'plain'))

        server.send_message(msg)
        server.quit()

        print_success("Test email sent successfully!")
        print_info("Check marvelmmk2005@gmail.com inbox")
        return True

    except Exception as e:
        print_error(f"SMTP test failed: {str(e)}")
        return False


def test_backend_email_endpoint():
    """Test backend email functionality through API"""
    print_header("TESTING BACKEND EMAIL VIA API")

    try:
        # First, register a user to trigger OTP email
        signup_data = {
            "name": "Marvel Test User",
            "email": "marvelmmk2005@gmail.com",
            "password": "TestPass123!"
        }

        print_info("Registering user to trigger OTP email...")
        response = requests.post(
            "http://127.0.0.1:5000/auth/signup", json=signup_data)

        if response.status_code == 201:
            print_success("User registration successful")
            result = response.json()
            user_id = result.get('id')
            print_info(f"User ID: {user_id}")

            if user_id:
                # Test resend OTP
                print_info("Testing resend OTP...")
                resend_data = {"user": user_id}
                resend_response = requests.post(
                    "http://127.0.0.1:5000/auth/resend-otp", json=resend_data)

                if resend_response.status_code == 200:
                    print_success("Resend OTP successful")
                    print_info("Check marvelmmk2005@gmail.com inbox for OTP")
                    return True
                else:
                    print_error(
                        f"Resend OTP failed: {resend_response.status_code}")
                    print_info(f"Response: {resend_response.text}")

        else:
            print_error(f"User registration failed: {response.status_code}")
            print_info(f"Response: {response.text}")

    except Exception as e:
        print_error(f"Backend email test failed: {str(e)}")
        return False


def check_backend_logs():
    """Instructions for checking backend logs"""
    print_header("CHECK BACKEND CONSOLE LOGS")
    print_info("In your Flask backend terminal, look for:")
    print_info("1. 'OTP sent to email: marvelmmk2005@gmail.com'")
    print_info("2. Any error messages about email sending")
    print_info("3. The actual OTP code (should be displayed)")
    print_info("4. SMTP connection status messages")


def main():
    """Run all email debug tests"""
    print_header("EMAIL SYSTEM DEBUG")

    # Test 1: Direct SMTP
    smtp_success = test_smtp_connection()

    # Test 2: Backend API
    if smtp_success:
        print_info("SMTP working, testing backend integration...")
        test_backend_email_endpoint()
    else:
        print_error("SMTP connection failed - check credentials")

    # Instructions for manual checking
    check_backend_logs()

    print_header("TROUBLESHOOTING TIPS")
    print_info("1. Check Gmail spam/junk folder")
    print_info("2. Verify 2-factor authentication is enabled on Gmail")
    print_info("3. Confirm app password is correct (not regular password)")
    print_info("4. Check Flask backend console for error messages")
    print_info("5. Try with a different email provider if needed")


if __name__ == "__main__":
    main()
