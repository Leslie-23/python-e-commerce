#!/usr/bin/env python3
"""
Server Status Check - Flask Backend & React Frontend
"""

import requests
import time


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


def check_flask_backend():
    """Check if Flask backend is running"""
    print_header("CHECKING FLASK BACKEND")

    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        if response.status_code == 200:
            print_success("Flask backend is running on http://127.0.0.1:5000")

            # Test a few key endpoints
            endpoints_to_test = [
                "/products",
                "/auth/login",  # This should be accessible
            ]

            for endpoint in endpoints_to_test:
                try:
                    test_response = requests.get(
                        f"http://127.0.0.1:5000{endpoint}", timeout=3)
                    print_info(
                        f"Endpoint {endpoint}: Status {test_response.status_code}")
                except:
                    print_info(f"Endpoint {endpoint}: Not accessible")

            return True
        else:
            print_error(
                f"Flask backend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Flask backend is NOT running")
        print_info("Please start Flask backend with: python run.py")
        return False
    except Exception as e:
        print_error(f"Error checking Flask backend: {str(e)}")
        return False


def check_react_frontend():
    """Check if React frontend is running"""
    print_header("CHECKING REACT FRONTEND")

    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print_success("React frontend is running on http://localhost:3000")
            return True
        else:
            print_error(
                f"React frontend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("React frontend is NOT running")
        print_info("Please start React frontend with: npm start")
        return False
    except Exception as e:
        print_error(f"Error checking React frontend: {str(e)}")
        return False


def provide_testing_instructions():
    """Provide step-by-step testing instructions"""
    print_header("OTP TESTING INSTRUCTIONS")

    print_info("📋 STEP-BY-STEP OTP TESTING:")
    print()

    print("🔹 STEP 1: REGISTER NEW USER")
    print("   1. Go to: http://localhost:3000")
    print("   2. Click 'Sign Up' or navigate to registration")
    print("   3. Register with email: marvelmmk2005@gmail.com")
    print("   4. Use password: TestPass123!")
    print("   5. Complete registration")
    print()

    print("🔹 STEP 2: OTP VERIFICATION")
    print("   1. After registration, you should be redirected to OTP verification")
    print("   2. Click 'Get OTP' or 'Send OTP'")
    print("   3. Check your email: marvelmmk2005@gmail.com")
    print("   4. Also check the Flask backend console for the OTP code")
    print("   5. Enter the OTP in the verification form")
    print("   6. Click 'Verify'")
    print()

    print("🔹 STEP 3: TEST LOGIN FLOW")
    print("   1. After successful verification, try logging out")
    print("   2. Log back in with: marvelmmk2005@gmail.com / TestPass123!")
    print("   3. Should login successfully without OTP (since verified)")
    print()

    print("🔹 ADMIN LOGIN TEST")
    print("   1. Log out from the regular user")
    print("   2. Login with admin credentials:")
    print("      Email: admin@example.com")
    print("      Password: admin123")
    print("   3. Should login directly without OTP")
    print()


def provide_troubleshooting():
    """Provide troubleshooting tips"""
    print_header("TROUBLESHOOTING TIPS")

    print("🔧 IF OTP EMAIL NOT RECEIVED:")
    print("   1. Check Gmail spam/junk folder")
    print("   2. Look at Flask backend console for OTP code")
    print("   3. Use console OTP if email doesn't arrive")
    print()

    print("🔧 IF SERVERS NOT RUNNING:")
    print("   Flask Backend:")
    print("   cd flask_backend")
    print("   python run.py")
    print()
    print("   React Frontend:")
    print("   cd frontend")
    print("   npm start")
    print()

    print("🔧 COMMON ISSUES:")
    print("   • User already exists: Use different email or remove existing user")
    print("   • Invalid OTP: Check for typos or request new OTP")
    print("   • Expired OTP: OTPs expire after 10 minutes")
    print("   • CORS errors: Make sure both servers are running")


def main():
    """Main function to check servers and provide instructions"""
    print_header("OTP FUNCTIONALITY TESTING SETUP")

    # Check both servers
    flask_running = check_flask_backend()
    react_running = check_react_frontend()

    print_header("SERVER STATUS SUMMARY")
    if flask_running:
        print_success("Flask Backend: RUNNING ✅")
    else:
        print_error("Flask Backend: NOT RUNNING ❌")

    if react_running:
        print_success("React Frontend: RUNNING ✅")
    else:
        print_error("React Frontend: NOT RUNNING ❌")

    print()

    if flask_running and react_running:
        print_success("🎉 BOTH SERVERS ARE RUNNING!")
        print_info("You can proceed with OTP testing")
        provide_testing_instructions()
    else:
        print_error("⚠️  Please start the missing server(s) first")

        if not flask_running:
            print_info("Start Flask: cd flask_backend && python run.py")
        if not react_running:
            print_info("Start React: cd frontend && npm start")

    provide_troubleshooting()


if __name__ == "__main__":
    main()
