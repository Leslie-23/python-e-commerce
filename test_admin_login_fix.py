#!/usr/bin/env python3

import requests
import json


def test_admin_login_response():
    """Test admin login to verify field mapping fix"""

    print("🧪 Testing Admin Login Field Mapping Fix")
    print("=" * 50)

    # Test admin login
    admin_login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/auth/login", json=admin_login_data)

        if response.status_code == 200:
            user_data = response.json()
            print("✅ Admin login successful!")
            print(f"📝 Response status: {response.status_code}")
            print("📋 User Data Fields:")

            # Check for both old and new field names
            for key, value in user_data.items():
                print(f"   {key}: {value}")

            # Specifically check the verification fields
            print("\n🔍 Field Mapping Verification:")
            if 'isVerified' in user_data:
                print(
                    f"   ✅ isVerified (camelCase): {user_data['isVerified']}")
            else:
                print("   ❌ isVerified (camelCase): NOT FOUND")

            if 'is_verified' in user_data:
                print(
                    f"   ⚠️  is_verified (snake_case): {user_data['is_verified']} (should be removed)")
            else:
                print("   ✅ is_verified (snake_case): CORRECTLY REMOVED")

            if 'isAdmin' in user_data:
                print(f"   ✅ isAdmin (camelCase): {user_data['isAdmin']}")
            else:
                print("   ❌ isAdmin (camelCase): NOT FOUND")

            if 'is_admin' in user_data:
                print(
                    f"   ⚠️  is_admin (snake_case): {user_data['is_admin']} (should be removed)")
            else:
                print("   ✅ is_admin (snake_case): CORRECTLY REMOVED")

            # Check if fix worked
            if user_data.get('isVerified') is True and 'is_verified' not in user_data:
                print("\n🎉 SUCCESS: Field mapping fix is working correctly!")
                print("   - Backend now returns 'isVerified' instead of 'is_verified'")
                print(
                    "   - Frontend should no longer redirect admin to OTP verification")
                return True
            else:
                print("\n❌ ISSUE: Field mapping fix needs adjustment")
                return False

        else:
            print(f"❌ Admin login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_admin_login_response()
    if success:
        print("\n✅ Test passed! The field mapping fix is working.")
        print("   Admin users should now be able to login without OTP redirection.")
    else:
        print("\n❌ Test failed! Check the field mapping implementation.")
