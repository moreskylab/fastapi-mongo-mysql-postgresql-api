#!/usr/bin/env python3
"""
Example usage of the FastAPI multi-database template

This script demonstrates how the template can be used by making API calls
to show the different database operations.
"""

import json
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime


async def demo_api_calls():
    """Demonstrate API calls to the FastAPI template"""
    
    print("FastAPI Multi-Database Template - API Demo")
    print("=" * 50)
    
    try:
        import httpx
        base_url = "http://localhost:8000"
        
        async with httpx.AsyncClient() as client:
            # Test root endpoint
            print("\n1. Testing root endpoint...")
            response = await client.get(f"{base_url}/")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # Test health endpoint
            print("\n2. Testing health endpoint...")
            response = await client.get(f"{base_url}/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
    except ImportError:
        print("\n⚠️  httpx not installed. Install with: pip install httpx")
    except Exception:
        print("\n⚠️  API server is not running.")
        print("To start the server:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Start databases: docker-compose up -d")  
        print("3. Run server: python main.py")
        print("4. Then run this demo again: python examples/api_demo.py")
    
    # Show API examples even if server is not running
    print("\n3. Example API calls (when server is running):")
    
    # Example MongoDB user creation
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }
    print(f"\nCreate user (MongoDB): POST /mongodb/users")
    print(f"Data: {json.dumps(user_data, indent=2)}")
    
    # Example MySQL product creation
    product_data = {
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": 999.99,
        "category": "Electronics"
    }
    print(f"\nCreate product (MySQL): POST /mysql/products")
    print(f"Data: {json.dumps(product_data, indent=2)}")
    
    # Example PostgreSQL order creation
    order_data = {
        "user_id": "user-uuid-here",
        "product_id": "product-uuid-here",
        "quantity": 2,
        "total_amount": 1999.98
    }
    print(f"\nCreate order (PostgreSQL): POST /postgresql/orders")
    print(f"Data: {json.dumps(order_data, indent=2)}")


def demo_without_server():
    """Show examples without requiring a running server"""
    print("\nFastAPI Multi-Database Template - Code Examples")
    print("=" * 50)
    
    # Show example model usage
    print("\n1. Pydantic Model Examples:")
    try:
        from app.models.schemas import UserCreate, ProductCreate, OrderCreate
        
        user = UserCreate(name="Alice Smith", email="alice@example.com", age=28)
        print(f"✓ User model: {user.model_dump()}")
        
        product = ProductCreate(
            name="Smartphone", 
            description="Latest smartphone", 
            price=699.99, 
            category="Electronics"
        )
        print(f"✓ Product model: {product.model_dump()}")
        
        order = OrderCreate(
            user_id="123e4567-e89b-12d3-a456-426614174000",
            product_id="123e4567-e89b-12d3-a456-426614174001", 
            quantity=1,
            total_amount=699.99
        )
        print(f"✓ Order model: {order.model_dump()}")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        
    # Show configuration example
    print("\n2. Configuration Example:")
    try:
        from app.core.config import get_settings
        settings = get_settings()
        print(f"✓ App name: {settings.app_name}")
        print(f"✓ MongoDB URL: {settings.mongodb_url}")
        print(f"✓ MySQL host: {settings.mysql_host}")
        print(f"✓ PostgreSQL host: {settings.postgresql_host}")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")


async def main():
    """Main demo function"""
    
    # Try API demo first
    await demo_api_calls()
    
    # Always show code examples
    demo_without_server()
    
    print("\n" + "=" * 50)
    print("Template Demo Complete!")
    print("\nNext steps:")
    print("1. Start databases: docker-compose up -d")
    print("2. Run the API: python main.py") 
    print("3. Visit: http://localhost:8000/docs")
    print("4. Try the interactive API documentation!")


if __name__ == "__main__":
    asyncio.run(main())