#!/usr/bin/env python3
"""
Test OTP Button Fix - Verify frontend field name fix works
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


def test_frontend_field_mapping():
    """Test that backend returns correct field names for frontend"""
    print_header("TESTING FRONTEND FIELD MAPPING")

    # Test login to get user data
    login_data = {
        "email": "marvelmmk2005@gmail.com",
        "password": "TestPass123!"
    }

    try:
        print_info("Testing login API response...")
        response = requests.post(
            "http://127.0.0.1:5000/auth/login", json=login_data)

        if response.status_code == 200:
            user_data = response.json()
            print_success("Login successful!")
            print_info(f"Response: {json.dumps(user_data, indent=2)}")

            # Check specific fields
            user_id = user_data.get('id')
            is_verified = user_data.get('isVerified')

            if user_id:
                print_success(f"✅ User ID found: {user_id}")
                print_info("Frontend can now use: loggedInUser?.id")
            else:
                print_error("❌ Missing 'id' field")

            if is_verified is not None:
                print_success(f"✅ isVerified found: {is_verified}")
                print_info("Frontend can now use: loggedInUser?.isVerified")
            else:
                print_error("❌ Missing 'isVerified' field")

            # Test OTP endpoint with correct field
            if user_id and not is_verified:
                print_info("\nTesting OTP endpoint with correct field...")
                otp_data = {"user": user_id}
                otp_response = requests.post(
                    "http://127.0.0.1:5000/auth/resend-otp", json=otp_data)

                if otp_response.status_code == 200:
                    print_success("🎉 OTP endpoint works with 'id' field!")
                    print_info("Frontend 'Get OTP' button should now work!")
                else:
                    print_error(f"OTP endpoint failed: {otp_response.status_code}")
            elif is_verified:
                print_info("User is verified - OTP not needed")

        else:
            print_error(f"Login failed: {response.status_code}")
            print_info(f"Response: {response.text}")

    except Exception as e:
        print_error(f"Test failed: {str(e)}")


def test_browser_instructions():
    """Provide instructions for testing in browser"""
    print_header("BROWSER TESTING INSTRUCTIONS")

    print_info("🌐 TO TEST THE FIX IN BROWSER:")
    print_info("1. Go to http://localhost:3000")
    print_info("2. Try to register a new user OR")
    print_info("3. Login with: marvelmmk2005@gmail.com / TestPass123!")
    print_info("4. If not verified, you'll be redirected to OTP page")
    print_info("5. Click 'Get OTP' button")
    print_info("6. Should work without 500 error now!")
    print_info("7. Check Flask backend console for OTP code")
    print_info("8. Enter the OTP to complete verification")

    print_header("WHAT WAS FIXED")
    print_success("✅ Fixed field name mismatch:")
    print_info("   - Changed loggedInUser?._id → loggedInUser?.id")
    print_info("   - This matches our sanitize_user.py field mapping")
    print_info("   - Backend now returns 'id' not '_id'")

    print_header("EXPECTED RESULTS")
    print_success("✅ 'Get OTP' button should work (no 500 error)")
    print_success("✅ OTP should appear in Flask backend console")
    print_success("✅ OTP verification should work")
    print_success("✅ User should be verified after entering OTP")


def main():
    """Main test function"""
    print_header("OTP BUTTON FIX VERIFICATION")
    
    test_frontend_field_mapping()
    test_browser_instructions()


if __name__ == "__main__":
    main()
