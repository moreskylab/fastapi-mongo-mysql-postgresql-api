#!/usr/bin/env python3
"""
Example usage script for FastAPI Multi-Database API

This script demonstrates how to interact with all three databases
through the API endpoints.
"""

import requests
import json
import time


def main():
    base_url = "http://localhost:8000"
    
    print("🚀 FastAPI Multi-Database API Demo")
    print("=" * 50)
    
    # Check if the API is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running!")
            print(f"📊 Response: {response.json()}")
        else:
            print("❌ API is not responding correctly")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("💡 Make sure the API is running: python main.py")
        return
    
    print("\n" + "=" * 50)
    print("📋 API Information")
    response = requests.get(f"{base_url}/")
    print(json.dumps(response.json(), indent=2))
    
    # Test data
    test_users = [
        {"name": "John Doe", "email": "john@example.com", "age": 30},
        {"name": "Jane Smith", "email": "jane@example.com", "age": 25},
        {"name": "Bob Johnson", "email": "bob@example.com", "age": 35}
    ]
    
    databases = ["mongodb", "mysql", "postgresql"]
    
    for db in databases:
        print(f"\n" + "=" * 50)
        print(f"🗄️  Testing {db.upper()} Database")
        print("=" * 50)
        
        endpoint = f"{base_url}/api/v1/{db}/users/"
        
        # Test GET (should be empty initially or error if DB not available)
        print(f"\n📖 GET {endpoint}")
        try:
            response = requests.get(endpoint)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                users = response.json()
                print(f"Users found: {len(users)}")
                if users:
                    print("Users:", json.dumps(users, indent=2))
                else:
                    print("No users found")
            else:
                print(f"Error: {response.json()}")
        except Exception as e:
            print(f"Request failed: {e}")
        
        # Test POST (create users)
        print(f"\n📝 POST {endpoint}")
        for i, user_data in enumerate(test_users):
            try:
                response = requests.post(endpoint, json=user_data)
                print(f"Creating user {i+1}: Status {response.status_code}")
                if response.status_code in [200, 201]:
                    created_user = response.json()
                    print(f"Created: {created_user.get('name', 'Unknown')} (ID: {created_user.get('id', 'N/A')})")
                else:
                    print(f"Error: {response.json()}")
                    break
            except Exception as e:
                print(f"Request failed: {e}")
                break
        
        # Test GET again (should show created users)
        print(f"\n📖 GET {endpoint} (after creation)")
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                users = response.json()
                print(f"Total users: {len(users)}")
                for user in users:
                    print(f"- {user.get('name', 'Unknown')} ({user.get('email', 'no-email')})")
            else:
                print(f"Error: {response.json()}")
        except Exception as e:
            print(f"Request failed: {e}")
    
    print(f"\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("💡 Visit http://localhost:8000/docs for interactive API documentation")
    print("💡 Visit http://localhost:8000/redoc for alternative documentation")


if __name__ == "__main__":
    main()