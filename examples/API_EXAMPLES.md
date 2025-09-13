# API Examples

Here are practical examples for using the FastAPI multi-database template:

## Quick Test Commands

### 1. Health Checks
```bash
# Application health
curl http://localhost:8000/health

# Database health checks
curl http://localhost:8000/mongodb/health
curl http://localhost:8000/mysql/health  
curl http://localhost:8000/postgresql/health
```

### 2. MongoDB Operations (Users)

```bash
# Create a user
curl -X POST "http://localhost:8000/mongodb/users" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "age": 30
     }'

# Get all users
curl http://localhost:8000/mongodb/users

# Get specific user
curl http://localhost:8000/mongodb/users/{user_id}

# Update user
curl -X PUT "http://localhost:8000/mongodb/users/{user_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Smith",
       "age": 31
     }'

# Delete user
curl -X DELETE http://localhost:8000/mongodb/users/{user_id}
```

### 3. MySQL Operations (Products)

```bash
# Create a product
curl -X POST "http://localhost:8000/mysql/products" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Laptop",
       "description": "High-performance laptop",
       "price": 999.99,
       "category": "Electronics"
     }'

# Get all products
curl http://localhost:8000/mysql/products

# Get specific product
curl http://localhost:8000/mysql/products/{product_id}

# Update product
curl -X PUT "http://localhost:8000/mysql/products/{product_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "price": 899.99,
       "description": "Discounted laptop"
     }'

# Delete product
curl -X DELETE http://localhost:8000/mysql/products/{product_id}
```

### 4. PostgreSQL Operations (Orders)

```bash
# Create an order
curl -X POST "http://localhost:8000/postgresql/orders" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user-uuid-here",
       "product_id": "product-uuid-here",
       "quantity": 2,
       "total_amount": 1999.98
     }'

# Get all orders
curl http://localhost:8000/postgresql/orders

# Get specific order
curl http://localhost:8000/postgresql/orders/{order_id}

# Update order
curl -X PUT "http://localhost:8000/postgresql/orders/{order_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "quantity": 3,
       "total_amount": 2999.97
     }'

# Delete order
curl -X DELETE http://localhost:8000/postgresql/orders/{order_id}
```

## Python Client Example

```python
import httpx
import asyncio

async def example_usage():
    async with httpx.AsyncClient() as client:
        # Create a user
        user_response = await client.post(
            "http://localhost:8000/mongodb/users",
            json={
                "name": "Alice Smith",
                "email": "alice@example.com",
                "age": 28
            }
        )
        user = user_response.json()
        print(f"Created user: {user['id']}")
        
        # Create a product
        product_response = await client.post(
            "http://localhost:8000/mysql/products",
            json={
                "name": "Smartphone",
                "description": "Latest smartphone",
                "price": 699.99,
                "category": "Electronics"
            }
        )
        product = product_response.json()
        print(f"Created product: {product['id']}")
        
        # Create an order
        order_response = await client.post(
            "http://localhost:8000/postgresql/orders",
            json={
                "user_id": user['id'],
                "product_id": product['id'],
                "quantity": 1,
                "total_amount": 699.99
            }
        )
        order = order_response.json()
        print(f"Created order: {order['id']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
```

## JavaScript/TypeScript Example

```javascript
// Using fetch API
async function createUser() {
    const response = await fetch('http://localhost:8000/mongodb/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: 'Bob Johnson',
            email: 'bob@example.com',
            age: 35
        })
    });
    
    const user = await response.json();
    console.log('Created user:', user);
    return user;
}

async function createProduct() {
    const response = await fetch('http://localhost:8000/mysql/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: 'Tablet',
            description: 'Portable tablet device',
            price: 399.99,
            category: 'Electronics'
        })
    });
    
    const product = await response.json();
    console.log('Created product:', product);
    return product;
}
```