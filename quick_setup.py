#!/usr/bin/env python3
"""
Quick Database Setup Script
Sets up your new MongoDB database with your Flask backend
"""

import os
import sys
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


def setup_database():
    """Setup and seed the new database using Flask seeding"""
    print_header("SETTING UP YOUR NEW MONGODB DATABASE")

    try:
        # Change to Flask backend directory
        flask_dir = os.path.join(os.path.dirname(__file__), 'flask_backend')
        original_dir = os.getcwd()
        os.chdir(flask_dir)

        print_info("Running database seeding script...")

        # Run the existing seed script
        import subprocess
        result = subprocess.run([sys.executable, 'seed_db.py'],
                                capture_output=True, text=True)

        if result.returncode == 0:
            print_success("Database seeded successfully!")
            print(result.stdout)
        else:
            print_error("Database seeding failed!")
            print(result.stderr)
            return False

        # Change back to original directory
        os.chdir(original_dir)
        return True

    except Exception as e:
        print_error(f"Setup failed: {e}")
        return False


def test_connection():
    """Test the new database connection"""
    print_header("TESTING DATABASE CONNECTION")

    try:
        import requests
        import time

        # Test if Flask backend is running
        base_url = "http://127.0.0.1:5000"

        print_info("Testing Flask backend connection...")
        response = requests.get(f"{base_url}/", timeout=5)

        if response.status_code == 200:
            print_success("Flask backend is running!")

            # Test products endpoint
            response = requests.get(f"{base_url}/products", timeout=5)
            if response.status_code == 200:
                products = response.json()
                print_success(
                    f"Products endpoint working - {len(products)} products found")

            # Test admin login
            login_data = {
                "email": "admin@example.com",
                "password": "admin123"
            }
            response = requests.post(
                f"{base_url}/auth/login", json=login_data, timeout=5)
            if response.status_code == 200:
                print_success("Admin login working!")
                print_info("Admin credentials: admin@example.com / admin123")

        else:
            print_error(
                f"Flask backend returned status: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to Flask backend.")
        print_info("Make sure to start the Flask server first:")
        print_info("cd flask_backend && python run.py")
    except Exception as e:
        print_error(f"Connection test failed: {e}")


def main():
    """Main function"""
    print_header("MONGODB DATABASE SETUP")
    print_info("Updated MongoDB URI to use your personal database")
    print_info(
        "Connection string: mongodb+srv://marvelmmk2005:***@cluster0.wxqvmph.mongodb.net/")

    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Setup/seed the database")
    print("2. Test database connection (Flask server must be running)")
    print("3. Both")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice in ['1', '3']:
        if setup_database():
            print_success("Database setup completed!")
        else:
            print_error("Database setup failed!")
            return

    if choice in ['2', '3']:
        test_connection()

    print_header("NEXT STEPS")
    print_info("1. Start Flask backend: cd flask_backend && python run.py")
    print_info("2. Start React frontend: cd frontend && npm start")
    print_info("3. Open http://localhost:3000")
    print_info("4. Test user registration and admin login")


if __name__ == "__main__":
    main()
