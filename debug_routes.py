#!/usr/bin/env python3
"""
Debug script to list all registered Flask routes
"""

import sys
sys.path.append('c:/Users/Marvel/python-e-commerce')

from webapp import app

def list_routes():
    """List all registered routes in the Flask app"""
    print("🔍 Registered Flask Routes")
    print("=" * 50)
    
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
        endpoint = rule.endpoint
        rule_str = str(rule)
        print(f"{rule_str:<30} {methods:<15} -> {endpoint}")
    
    print("=" * 50)
    print(f"Total routes: {len(list(app.url_map.iter_rules()))}")

if __name__ == "__main__":
    list_routes()