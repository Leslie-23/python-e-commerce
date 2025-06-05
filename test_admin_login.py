#!/usr/bin/env python3
"""
Simple admin login test
"""

import requests
import sys

BASE_URL = "http://127.0.0.1:5007"

def test_admin_login_and_access():
    session = requests.Session()
    
    print("🔍 Testing Admin Access Step by Step")
    print("=" * 50)
    
    # Step 1: Get login page
    print("Step 1: Accessing login page...")
    login_page = session.get(f"{BASE_URL}/login/")
    print(f"Login page status: {login_page.status_code}")
    
    # Step 2: Submit login
    print("\nStep 2: Submitting admin credentials...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    login_response = session.post(f"{BASE_URL}/login/", data=login_data, allow_redirects=False)
    print(f"Login response status: {login_response.status_code}")
    print(f"Login response headers: {dict(login_response.headers)}")
    
    if login_response.status_code == 302:
        print(f"Redirect location: {login_response.headers.get('Location', 'None')}")
      # Step 3: Follow redirect if any
    if login_response.status_code == 302:
        print("\nStep 3: Following redirect...")
        redirect_location = login_response.headers['Location']
        if redirect_location.startswith('/'):
            redirect_location = BASE_URL + redirect_location
        redirect_response = session.get(redirect_location)
        print(f"Redirect response status: {redirect_response.status_code}")
    
    # Step 4: Test direct admin access
    print("\nStep 4: Testing direct admin access...")
    admin_response = session.get(f"{BASE_URL}/admin")
    print(f"Admin response status: {admin_response.status_code}")
    
    if admin_response.status_code == 302:
        print(f"Admin redirect location: {admin_response.headers.get('Location', 'None')}")
    elif admin_response.status_code == 200:
        print("✅ Admin access successful!")
        return True
    else:
        print(f"❌ Admin access failed with status {admin_response.status_code}")
        # Print first 500 characters of response for debugging
        print("Response content preview:")
        print(admin_response.text[:500])
    
    return False

if __name__ == "__main__":
    test_admin_login_and_access()
