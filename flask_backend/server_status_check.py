#!/usr/bin/env python3
"""
Server Status Check - Verify both frontend and backend are running
"""

import requests
import sys

def check_servers():
    """Check if both frontend and backend servers are running"""
    
    print("🔄 Checking Server Status")
    print("=" * 30)
    
    # Check Flask backend
    try:
        backend_response = requests.get("http://localhost:5000/", timeout=5)
        if backend_response.status_code == 200:
            print("✅ Flask Backend: Running on http://localhost:5000")
        else:
            print(f"❌ Flask Backend: Unexpected status {backend_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Flask Backend: Not running or unreachable - {e}")
        return False
    
    # Check React frontend on common ports
    frontend_ports = [3000, 3001, 3002, 3003]
    frontend_running = False
    
    for port in frontend_ports:
        try:
            frontend_response = requests.get(f"http://localhost:{port}/", timeout=5)
            if frontend_response.status_code == 200:
                print(f"✅ React Frontend: Running on http://localhost:{port}")
                frontend_running = True
                break
        except requests.exceptions.RequestException:
            continue
    
    if not frontend_running:
        print("❌ React Frontend: Not found on common ports")
        return False
    
    print("\n🎉 Both servers are running!")
    print("\n📋 Next Steps:")
    print("   1. Open the React app in your browser")
    print("   2. Navigate to the login page")
    print("   3. Use credentials: admin@example.com / admin123")
    print("   4. You should be able to login successfully!")
    
    return True

if __name__ == "__main__":
    success = check_servers()
    if not success:
        print("\n❌ Please ensure both servers are running before testing login")
        sys.exit(1)
