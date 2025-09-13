#!/usr/bin/env python3
"""
Test script to validate the FastAPI application structure
This script tests the application without requiring actual database connections
"""

import sys
import traceback


def test_imports():
    """Test all critical imports"""
    try:
        print("Testing imports...")
        
        # Test core imports
        from app.core.config import get_settings
        print("✓ Core config import successful")
        
        # Test model imports
        from app.models.schemas import UserCreate, ProductCreate, OrderCreate, HealthCheck
        print("✓ Schema imports successful")
        
        # Test database modules (without connecting)
        from app.db import mongodb, mysql, postgresql
        print("✓ Database module imports successful")
        
        # Test API routes
        from app.api import mongodb_routes, mysql_routes, postgresql_routes
        print("✓ API route imports successful")
        
        # Test main application
        from main import app
        print("✓ Main application import successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False


def test_config():
    """Test configuration"""
    try:
        print("\nTesting configuration...")
        from app.core.config import get_settings
        
        settings = get_settings()
        assert settings.app_name
        assert settings.mongodb_url
        assert settings.mysql_host
        assert settings.postgresql_host
        
        print("✓ Configuration validation successful")
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_models():
    """Test Pydantic models"""
    try:
        print("\nTesting Pydantic models...")
        from app.models.schemas import UserCreate, ProductCreate, OrderCreate
        
        # Test UserCreate
        user = UserCreate(name="Test User", email="test@example.com", age=25)
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.age == 25
        
        # Test ProductCreate
        product = ProductCreate(
            name="Test Product",
            description="A test product",
            price=99.99,
            category="Test"
        )
        assert product.name == "Test Product"
        assert product.price == 99.99
        
        # Test OrderCreate
        order = OrderCreate(
            user_id="user-123",
            product_id="product-456",
            quantity=2,
            total_amount=199.98
        )
        assert order.quantity == 2
        assert order.total_amount == 199.98
        
        print("✓ Pydantic model validation successful")
        return True
        
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False


def test_fastapi_app():
    """Test FastAPI application creation"""
    try:
        print("\nTesting FastAPI application...")
        from main import app
        
        # Check that app is created
        assert app is not None
        assert hasattr(app, 'routes')
        
        # Check that routers are included
        routes = [route.path for route in app.routes]
        
        # Should have root route
        assert "/" in routes
        assert "/health" in routes
        
        print("✓ FastAPI application structure validation successful")
        return True
        
    except Exception as e:
        print(f"✗ FastAPI application test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("FastAPI Multi-Database Template - Structure Validation")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_models,
        test_fastapi_app
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
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Tests completed: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✓ All structure validation tests passed!")
        print("✓ FastAPI template is ready for use!")
        return 0
    else:
        print("✗ Some tests failed. Please check the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())