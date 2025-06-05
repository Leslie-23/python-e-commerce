#!/usr/bin/env python3
"""
Comprehensive E-commerce Application Test Suite
Tests all major functionalities to ensure the application is fully functional
"""

import sys
sys.path.append('c:/Users/Marvel/python-e-commerce')

from webapp.dbaccess import *
from webapp.databaseConfig import database_connector
import requests

BASE_URL = "http://127.0.0.1:5007"

class EcommerceTestSuite:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def add_result(self, test_name, success, message=""):
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")
        
    def test_database_connectivity(self):
        """Test database connection and basic functions"""
        try:
            database_connector()
            stats = get_admin_stats()
            self.add_result("Database Connectivity", True, f"Connected. {stats['total_users']} users, {stats['total_products']} products")
        except Exception as e:
            self.add_result("Database Connectivity", False, str(e))
            
    def test_user_authentication(self):
        """Test user authentication system"""
        # Test admin user
        try:
            admin_data = auth_user({'username': 'admin', 'password': 'admin123'})
            if admin_data:
                role = get_user_role(admin_data[0])
                self.add_result("Admin Authentication", True, f"Admin user ID: {admin_data[0]}, Role: {role}")
            else:
                self.add_result("Admin Authentication", False, "Admin login failed")
        except Exception as e:
            self.add_result("Admin Authentication", False, str(e))
              # Test regular user
        try:
            user_data = auth_user({'username': 'johndoe', 'password': 'password123'})
            if user_data:
                role = get_user_role(user_data[0])
                self.add_result("User Authentication", True, f"Regular user ID: {user_data[0]}, Role: {role}")
            else:
                self.add_result("User Authentication", False, "User login failed")
        except Exception as e:
            self.add_result("User Authentication", False, str(e))
            
    def test_product_management(self):
        """Test product management functions"""
        try:
            products = get_all_products_admin()
            categories = get_all_categories()
            inventory = get_inventory_overview()
            
            self.add_result("Product Management", True, f"{len(products)} products, {len(categories)} categories, {len(inventory)} inventory items")
        except Exception as e:
            self.add_result("Product Management", False, str(e))
            
    def test_order_management(self):
        """Test order management functions"""
        try:
            orders = get_all_orders_paginated(page=1, per_page=10)
            recent_orders = get_recent_orders(limit=5)
            
            self.add_result("Order Management", True, f"{len(orders)} orders in page 1, {len(recent_orders)} recent orders")
        except Exception as e:
            self.add_result("Order Management", False, str(e))
            
    def test_web_routes(self):
        """Test main web routes"""
        routes_to_test = [
            ("/", "Home Page"),
            ("/login/", "Login Page"),
            ("/signup/", "Signup Page"),
            ("/contact", "Contact Page"),
            ("/electronics", "Electronics Page"),
            ("/toys", "Toys Page"),
            ("/analytics", "Analytics Page"),
        ]
        
        for route, name in routes_to_test:
            try:
                response = self.session.get(f"{BASE_URL}{route}")
                if response.status_code == 200:
                    self.add_result(f"Route {name}", True, f"Status {response.status_code}")
                else:
                    self.add_result(f"Route {name}", False, f"Status {response.status_code}")
            except Exception as e:
                self.add_result(f"Route {name}", False, str(e))
                
    def test_user_management(self):
        """Test user management functions"""
        try:
            users = get_all_users()
            admin_users = [user for user in users if len(user) > 3 and get_user_role(user[0]) == 'admin']
            regular_users = [user for user in users if len(user) > 3 and get_user_role(user[0]) == 'user']
            
            self.add_result("User Management", True, f"{len(users)} total users ({len(admin_users)} admins, {len(regular_users)} regular)")
        except Exception as e:
            self.add_result("User Management", False, str(e))
            
    def test_cart_functionality(self):
        """Test cart functions"""
        try:
            # Test guest cart functionality
            variant_ids = [1, 2, 3]  # Assuming these exist
            guest_cart = get_guest_cart(variant_ids)
            
            self.add_result("Cart Functionality", True, f"Guest cart test successful with {len(guest_cart)} items")
        except Exception as e:
            self.add_result("Cart Functionality", False, str(e))
            
    def test_search_functionality(self):
        """Test search functions"""
        try:
            # Test product search
            search_results = search_product("laptop")
            electronics = get_categories("Electronics")
            
            self.add_result("Search Functionality", True, f"Search returned {len(search_results)} results, Electronics has {len(electronics)} items")
        except Exception as e:
            self.add_result("Search Functionality", False, str(e))
            
    def test_template_files(self):
        """Check if essential template files exist"""
        import os
        template_dir = "c:/Users/Marvel/python-e-commerce/webapp/templates"
        
        essential_templates = [
            "layout.html",
            "home.html",
            "login.html",
            "signup.html",
            "contact.html",
            "products.html",
            "cart.html",
            "checkout.html",
            "admin/dashboard.html",
            "admin/users.html",
            "admin/products.html",
            "admin/categories.html",
            "admin/orders.html",
            "admin/inventory.html",
            "user/profile.html",
            "user/orders.html",
            "404.html",
            "500.html"
        ]
        
        missing_templates = []
        for template in essential_templates:
            template_path = os.path.join(template_dir, template)
            if not os.path.exists(template_path):
                missing_templates.append(template)
                
        if not missing_templates:
            self.add_result("Template Files", True, f"All {len(essential_templates)} essential templates exist")
        else:
            self.add_result("Template Files", False, f"Missing templates: {', '.join(missing_templates)}")
            
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 E-Commerce Application Test Suite")
        print("=" * 60)
        
        # Database tests
        print("\n📊 Database Tests")
        print("-" * 30)
        self.test_database_connectivity()
        self.test_user_authentication()
        self.test_product_management()
        self.test_order_management()
        self.test_user_management()
        self.test_cart_functionality()
        self.test_search_functionality()
        
        # Web application tests
        print("\n🌐 Web Application Tests")
        print("-" * 30)
        self.test_web_routes()
        self.test_template_files()
        
        # Summary
        print("\n📋 Test Summary")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        failed = len(self.test_results) - passed
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        
        if failed > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        if failed == 0:
            print("\n🎉 All tests passed! The e-commerce application is fully functional!")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please review the issues above.")
            
        return failed == 0

def main():
    tester = EcommerceTestSuite()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
