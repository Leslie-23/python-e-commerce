#!/usr/bin/env python3
"""
Test script for admin functionalities
Tests all admin panel features to ensure they work correctly
"""

import requests
import json
import sys
from datetime import datetime

# Base URL for the application
BASE_URL = "http://127.0.0.1:5007"

class AdminTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_logged_in = False
        
    def login_admin(self, username="admin", password="admin123"):
        """Login as admin user"""
        login_data = {
            'username': username,
            'password': password
        }
        
        response = self.session.post(f"{BASE_URL}/login/", data=login_data)
        
        if response.status_code == 200 and "admin" in response.text.lower():
            self.admin_logged_in = True
            print("✅ Admin login successful")
            return True
        else:
            print("❌ Admin login failed")
            return False
            
    def test_admin_dashboard(self):
        """Test admin dashboard access"""
        if not self.admin_logged_in:
            print("❌ Not logged in as admin")
            return False
            
        response = self.session.get(f"{BASE_URL}/admin")
        
        if response.status_code == 200:
            print("✅ Admin dashboard accessible")
            return True
        else:
            print(f"❌ Admin dashboard failed with status {response.status_code}")
            return False
            
    def test_admin_users(self):
        """Test admin users management page"""
        response = self.session.get(f"{BASE_URL}/admin/users")
        
        if response.status_code == 200:
            print("✅ Admin users page accessible")
            return True
        else:
            print(f"❌ Admin users page failed with status {response.status_code}")
            return False
            
    def test_admin_products(self):
        """Test admin products management page"""
        response = self.session.get(f"{BASE_URL}/admin/products")
        
        if response.status_code == 200:
            print("✅ Admin products page accessible")
            return True
        else:
            print(f"❌ Admin products page failed with status {response.status_code}")
            return False
            
    def test_admin_categories(self):
        """Test admin categories management page"""
        response = self.session.get(f"{BASE_URL}/admin/categories")
        
        if response.status_code == 200:
            print("✅ Admin categories page accessible")
            return True
        else:
            print(f"❌ Admin categories page failed with status {response.status_code}")
            return False
            
    def test_admin_orders(self):
        """Test admin orders management page"""
        response = self.session.get(f"{BASE_URL}/admin/orders")
        
        if response.status_code == 200:
            print("✅ Admin orders page accessible")
            return True
        else:
            print(f"❌ Admin orders page failed with status {response.status_code}")
            return False
            
    def test_admin_inventory(self):
        """Test admin inventory management page"""
        response = self.session.get(f"{BASE_URL}/admin/inventory")
        
        if response.status_code == 200:
            print("✅ Admin inventory page accessible")
            return True
        else:
            print(f"❌ Admin inventory page failed with status {response.status_code}")
            return False
            
    def test_admin_analytics(self):
        """Test admin analytics page"""
        response = self.session.get(f"{BASE_URL}/admin/analytics")
        
        if response.status_code == 200:
            print("✅ Admin analytics page accessible")
            return True
        else:
            print(f"❌ Admin analytics page failed with status {response.status_code}")
            return False
            
    def test_admin_settings(self):
        """Test admin settings page"""
        response = self.session.get(f"{BASE_URL}/admin/settings")
        
        if response.status_code == 200:
            print("✅ Admin settings page accessible")
            return True
        else:
            print(f"❌ Admin settings page failed with status {response.status_code}")
            return False
            
    def test_add_product_page(self):
        """Test add product page"""
        response = self.session.get(f"{BASE_URL}/admin/products/add")
        
        if response.status_code == 200:
            print("✅ Add product page accessible")
            return True
        else:
            print(f"❌ Add product page failed with status {response.status_code}")
            return False
            
    def test_add_category_page(self):
        """Test add category page"""
        response = self.session.get(f"{BASE_URL}/admin/categories/add")
        
        if response.status_code == 200:
            print("✅ Add category page accessible")
            return True
        else:
            print(f"❌ Add category page failed with status {response.status_code}")
            return False
            
    def test_api_admin_stats(self):
        """Test admin stats API"""
        response = self.session.get(f"{BASE_URL}/api/admin/stats")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Admin stats API working")
                return True
            except:
                print("❌ Admin stats API returned invalid JSON")
                return False
        else:
            print(f"❌ Admin stats API failed with status {response.status_code}")
            return False
            
    def test_cart_count_api(self):
        """Test cart count API"""
        response = self.session.get(f"{BASE_URL}/api/cart/count")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Cart count API working")
                return True
            except:
                print("❌ Cart count API returned invalid JSON")
                return False
        else:
            print(f"❌ Cart count API failed with status {response.status_code}")
            return False
            
    def test_user_profile_access(self):
        """Test user profile pages"""
        # Test user profile
        response = self.session.get(f"{BASE_URL}/profile")
        if response.status_code == 200:
            print("✅ User profile page accessible")
        else:
            print(f"❌ User profile page failed with status {response.status_code}")
            
        # Test edit profile
        response = self.session.get(f"{BASE_URL}/profile/edit")
        if response.status_code == 200:
            print("✅ Edit profile page accessible")
        else:
            print(f"❌ Edit profile page failed with status {response.status_code}")
            
        # Test user orders
        response = self.session.get(f"{BASE_URL}/orders")
        if response.status_code == 200:
            print("✅ User orders page accessible")
        else:
            print(f"❌ User orders page failed with status {response.status_code}")
            
        # Test change password
        response = self.session.get(f"{BASE_URL}/profile/change-password")
        if response.status_code == 200:
            print("✅ Change password page accessible")
        else:
            print(f"❌ Change password page failed with status {response.status_code}")
    
    def run_all_tests(self):
        """Run all admin functionality tests"""
        print("🔍 Starting Admin Panel Tests")
        print("=" * 50)
        
        if not self.login_admin():
            print("❌ Cannot proceed with tests - Admin login failed")
            return False
            
        tests = [
            self.test_admin_dashboard,
            self.test_admin_users,
            self.test_admin_products,
            self.test_admin_categories,
            self.test_admin_orders,
            self.test_admin_inventory,
            self.test_admin_analytics,
            self.test_admin_settings,
            self.test_add_product_page,
            self.test_add_category_page,
            self.test_api_admin_stats,
            self.test_cart_count_api,
            self.test_user_profile_access
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {e}")
                failed += 1
        
        print("=" * 50)
        print(f"📊 Test Results: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All tests passed! Admin panel is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the output above for details.")
            
        return failed == 0

def main():
    """Main test function"""
    print("🚀 E-Commerce Admin Panel Testing")
    print("=" * 50)
    
    tester = AdminTester()
    success = tester.run_all_tests()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
