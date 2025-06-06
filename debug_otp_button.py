#!/usr/bin/env python3
"""
Debug OTP Button Issue - Check API and Frontend Logs
"""

import requests
import json


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


def test_get_otp_directly():
    """Test the OTP endpoint directly to see if it works"""
    print_header("TESTING GET OTP API DIRECTLY")

    # First, let's find the user ID for marvelmmk2005@gmail.com
    login_data = {
        "email": "marvelmmk2005@gmail.com",
        "password": "TestPass123!"
    }

    try:
        print_info("Step 1: Getting user ID via login...")
        login_response = requests.post(
            "http://127.0.0.1:5000/auth/login", json=login_data)

        if login_response.status_code == 200:
            user_data = login_response.json()
            user_id = user_data.get('id')
            is_verified = user_data.get('isVerified')

            print_success(f"User found - ID: {user_id}")
            print_info(f"Verified status: {is_verified}")

            if user_id and not is_verified:
                print_info("Step 2: Testing resend-otp endpoint...")

                # Test the resend-otp endpoint
                otp_data = {"user": user_id}
                headers = {'Content-Type': 'application/json'}

                print_info(
                    f"Sending request to: http://127.0.0.1:5000/auth/resend-otp")
                print_info(f"Request data: {otp_data}")

                otp_response = requests.post(
                    "http://127.0.0.1:5000/auth/resend-otp",
                    json=otp_data,
                    headers=headers
                )

                print_info(f"Response status: {otp_response.status_code}")
                print_info(f"Response headers: {dict(otp_response.headers)}")
                print_info(f"Response body: {otp_response.text}")

                if otp_response.status_code == 200:
                    print_success("🎉 OTP API is working correctly!")
                    print_info("The issue is likely on the frontend side")
                else:
                    print_error("OTP API is failing")

            elif is_verified:
                print_info("User is already verified - no OTP needed")
            else:
                print_error("No user ID found")

        else:
            print_error(f"Login failed: {login_response.status_code}")
            print_info(f"Response: {login_response.text}")

    except Exception as e:
        print_error(f"API test failed: {str(e)}")


def check_cors_headers():
    """Check CORS configuration"""
    print_header("CHECKING CORS CONFIGURATION")

    try:
        # Test CORS preflight
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }

        response = requests.options(
            "http://127.0.0.1:5000/auth/resend-otp", headers=headers)

        print_info(f"CORS preflight status: {response.status_code}")
        print_info(f"CORS headers: {dict(response.headers)}")

        # Check if CORS headers are present
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers'
        ]

        for header in cors_headers:
            if header in response.headers:
                print_success(f"{header}: {response.headers[header]}")
            else:
                print_error(f"Missing CORS header: {header}")

    except Exception as e:
        print_error(f"CORS check failed: {str(e)}")


def provide_frontend_debugging_tips():
    """Provide frontend debugging instructions"""
    print_header("FRONTEND DEBUGGING INSTRUCTIONS")

    print_info("🔍 CHECK BROWSER DEVELOPER TOOLS:")
    print("1. Open browser (Chrome/Firefox)")
    print("2. Go to http://localhost:3000")
    print("3. Press F12 to open Developer Tools")
    print("4. Go to 'Console' tab")
    print("5. Navigate to OTP verification page")
    print("6. Click 'Get OTP' button")
    print("7. Look for any error messages in console")
    print()

    print_info("🌐 CHECK NETWORK TAB:")
    print("1. In Developer Tools, go to 'Network' tab")
    print("2. Click 'Get OTP' button")
    print("3. Look for:")
    print("   - POST request to /auth/resend-otp")
    print("   - Request status (200, 404, 500, etc.)")
    print("   - Request/Response data")
    print("   - Any failed requests (red)")
    print()

    print_info("🚨 COMMON ISSUES TO LOOK FOR:")
    print("• JavaScript errors in console")
    print("• CORS errors")
    print("• Network request failures")
    print("• 404 errors (wrong API endpoint)")
    print("• Authentication/token issues")
    print()

    print_info("📱 WHAT TO REPORT BACK:")
    print("1. Any error messages from browser console")
    print("2. Network request status and response")
    print("3. Whether the request is being sent at all")


def main():
    """Main debugging function"""
    print_header("OTP BUTTON DEBUG")

    # Test the API directly
    test_get_otp_directly()

    # Check CORS
    check_cors_headers()

    # Provide frontend debugging tips
    provide_frontend_debugging_tips()

    print_header("NEXT STEPS")
    print_info("1. Run this script to verify API is working")
    print_info("2. Check browser developer tools as instructed above")
    print_info("3. Report back any errors you find")
    print_info("4. If API works but frontend doesn't, it's a React issue")


if __name__ == "__main__":
    main()
