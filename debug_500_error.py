#!/usr/bin/env python3
"""
Debug 500 Error on OTP Endpoint
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

def test_different_request_formats():
    """Test different ways the frontend might be calling the API"""
    print_header("TESTING DIFFERENT REQUEST FORMATS")
    
    # Get user ID first
    login_data = {
        "email": "marvelmmk2005@gmail.com",
        "password": "TestPass123!"
    }
    
    try:
        login_response = requests.post("http://127.0.0.1:5000/auth/login", json=login_data)
        if login_response.status_code == 200:
            user_data = login_response.json()
            user_id = user_data.get('id')
            print_success(f"Got user ID: {user_id}")
            
            # Test 1: Standard format (what worked before)
            print_info("Test 1: Standard JSON format")
            test_standard_format(user_id)
            
            # Test 2: Different content-type
            print_info("Test 2: With explicit content-type")
            test_with_headers(user_id)
            
            # Test 3: Form data (in case frontend sends this)
            print_info("Test 3: Form data format")
            test_form_data(user_id)
            
            # Test 4: Different JSON structure
            print_info("Test 4: Different JSON structure")
            test_different_json(user_id)
            
        else:
            print_error(f"Login failed: {login_response.status_code}")
            
    except Exception as e:
        print_error(f"Error in test: {str(e)}")

def test_standard_format(user_id):
    """Test the standard format that worked before"""
    try:
        data = {"user": user_id}
        response = requests.post("http://127.0.0.1:5000/auth/resend-otp", json=data)
        print_info(f"Standard format - Status: {response.status_code}")
        if response.status_code != 200:
            print_error(f"Response: {response.text}")
        else:
            print_success("Standard format works")
    except Exception as e:
        print_error(f"Standard format error: {str(e)}")

def test_with_headers(user_id):
    """Test with explicit headers"""
    try:
        data = {"user": user_id}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.post("http://127.0.0.1:5000/auth/resend-otp", json=data, headers=headers)
        print_info(f"With headers - Status: {response.status_code}")
        if response.status_code != 200:
            print_error(f"Response: {response.text}")
        else:
            print_success("With headers works")
    except Exception as e:
        print_error(f"With headers error: {str(e)}")

def test_form_data(user_id):
    """Test with form data"""
    try:
        data = {"user": user_id}
        response = requests.post("http://127.0.0.1:5000/auth/resend-otp", data=data)
        print_info(f"Form data - Status: {response.status_code}")
        if response.status_code != 200:
            print_error(f"Response: {response.text}")
        else:
            print_success("Form data works")
    except Exception as e:
        print_error(f"Form data error: {str(e)}")

def test_different_json(user_id):
    """Test with different JSON structure"""
    try:
        # Test with userId instead of user
        data = {"userId": user_id}
        response = requests.post("http://127.0.0.1:5000/auth/resend-otp", json=data)
        print_info(f"userId field - Status: {response.status_code}")
        if response.status_code != 200:
            print_error(f"Response: {response.text}")
        
        # Test with user_id instead of user
        data = {"user_id": user_id}
        response = requests.post("http://127.0.0.1:5000/auth/resend-otp", json=data)
        print_info(f"user_id field - Status: {response.status_code}")
        if response.status_code != 200:
            print_error(f"Response: {response.text}")
            
    except Exception as e:
        print_error(f"Different JSON error: {str(e)}")

def check_backend_error_logs():
    """Instructions for checking backend error logs"""
    print_header("CHECK FLASK BACKEND CONSOLE")
    print_info("Look in your Flask backend terminal for:")
    print("• Error traceback/stack trace")
    print("• 500 Internal Server Error details")
    print("• Any Python exception messages")
    print("• Database connection errors")
    print("• Authentication/token errors")
    print()
    print_info("Common 500 error causes:")
    print("• Missing required fields in request")
    print("• Database connection issues")
    print("• Email service configuration problems")
    print("• Authentication/user validation errors")
    print("• JSON parsing errors")

def main():
    """Main debugging function"""
    print_header("DEBUG 500 INTERNAL SERVER ERROR")
    
    test_different_request_formats()
    check_backend_error_logs()
    
    print_header("NEXT STEPS")
    print_info("1. Check Flask backend console for detailed error messages")
    print_info("2. Look for Python traceback/exception details")
    print_info("3. Copy and paste any error messages you see")
    print_info("4. Check if the error happens consistently")

if __name__ == "__main__":
    main()
