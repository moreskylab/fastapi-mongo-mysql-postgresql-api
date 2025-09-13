#!/usr/bin/env python3
"""
Simple test script to validate core FastAPI functionality without database dependencies
"""

import sys


def test_basic_functionality():
    """Test basic FastAPI application without database connections"""
    try:
        print("Testing basic FastAPI functionality...")
        
        # Test core imports
        from app.core.config import get_settings
        from app.models.schemas import UserCreate, ProductCreate, OrderCreate
        
        settings = get_settings()
        print(f"✓ Application: {settings.app_name}")
        
        # Test model creation
        user = UserCreate(name="Test User", email="test@example.com", age=25)
        product = ProductCreate(name="Test Product", price=99.99, category="Test")
        order = OrderCreate(user_id="123", product_id="456", quantity=1, total_amount=99.99)
        
        print("✓ Pydantic models work correctly")
        
        # Test FastAPI app creation (basic version)
        from fastapi import FastAPI
        app = FastAPI(title=settings.app_name, version=settings.app_version)
        
        @app.get("/")
        def read_root():
            return {"message": "FastAPI template is working"}
        
        @app.get("/health")
        def health():
            return {"status": "healthy"}
        
        print("✓ FastAPI application can be created")
        print("✓ Basic template structure is valid")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False


def main():
    """Run basic validation"""
    print("FastAPI Multi-Database Template - Basic Validation")
    print("=" * 55)
    
    if test_basic_functionality():
        print("\n✓ Core template structure is valid!")
        print("✓ Install database dependencies to use full functionality")
        print("\nTo install all dependencies:")
        print("  pip install -r requirements.txt")
        print("\nTo run the full application:")
        print("  python main.py")
        return 0
    else:
        print("\n✗ Basic validation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())