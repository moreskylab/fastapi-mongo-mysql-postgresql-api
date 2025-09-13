from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from datetime import datetime
from app.models.schemas import OrderCreate, OrderUpdate, OrderResponse, HealthCheck
from app.db.postgresql import get_postgresql_connection

router = APIRouter(prefix="/postgresql", tags=["PostgreSQL"])


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check for PostgreSQL"""
    try:
        async with get_postgresql_connection() as connection:
            await connection.execute("SELECT 1")
        return HealthCheck(
            status="healthy",
            database="PostgreSQL",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"PostgreSQL health check failed: {str(e)}"
        )


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """Create a new order in PostgreSQL"""
    try:
        order_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        
        async with get_postgresql_connection() as connection:
            await connection.execute("""
                INSERT INTO orders (id, user_id, product_id, quantity, total_amount, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, order_id, order.user_id, order.product_id, order.quantity, 
                order.total_amount, created_at, created_at)
            
        return OrderResponse(
            id=order_id,
            user_id=order.user_id,
            product_id=order.product_id,
            quantity=order.quantity,
            total_amount=order.total_amount,
            created_at=created_at,
            updated_at=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating order: {str(e)}"
        )


@router.get("/orders", response_model=List[OrderResponse])
async def get_orders():
    """Get all orders from PostgreSQL"""
    try:
        async with get_postgresql_connection() as connection:
            rows = await connection.fetch("""
                SELECT id, user_id, product_id, quantity, total_amount, created_at, updated_at
                FROM orders
                ORDER BY created_at DESC
            """)
            
            orders = []
            for row in rows:
                orders.append(OrderResponse(
                    id=row['id'],
                    user_id=row['user_id'],
                    product_id=row['product_id'],
                    quantity=row['quantity'],
                    total_amount=float(row['total_amount']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
            return orders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching orders: {str(e)}"
        )


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """Get a specific order by ID from PostgreSQL"""
    try:
        async with get_postgresql_connection() as connection:
            row = await connection.fetchrow("""
                SELECT id, user_id, product_id, quantity, total_amount, created_at, updated_at
                FROM orders WHERE id = $1
            """, order_id)
            
            if row:
                return OrderResponse(
                    id=row['id'],
                    user_id=row['user_id'],
                    product_id=row['product_id'],
                    quantity=row['quantity'],
                    total_amount=float(row['total_amount']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching order: {str(e)}"
        )


@router.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: str, order_update: OrderUpdate):
    """Update an order in PostgreSQL"""
    try:
        update_fields = []
        values = []
        param_count = 1
        
        # Build dynamic update query
        for field, value in order_update.dict().items():
            if value is not None:
                update_fields.append(f"{field} = ${param_count}")
                values.append(value)
                param_count += 1
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
        
        # Add updated_at field
        update_fields.append(f"updated_at = ${param_count}")
        values.append(datetime.utcnow())
        param_count += 1
        values.append(order_id)
        
        async with get_postgresql_connection() as connection:
            query = f"UPDATE orders SET {', '.join(update_fields)} WHERE id = ${param_count}"
            result = await connection.execute(query, *values)
            
            if result == "UPDATE 0":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            # Fetch updated order
            row = await connection.fetchrow("""
                SELECT id, user_id, product_id, quantity, total_amount, created_at, updated_at
                FROM orders WHERE id = $1
            """, order_id)
            
            return OrderResponse(
                id=row['id'],
                user_id=row['user_id'],
                product_id=row['product_id'],
                quantity=row['quantity'],
                total_amount=float(row['total_amount']),
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating order: {str(e)}"
        )


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str):
    """Delete an order from PostgreSQL"""
    try:
        async with get_postgresql_connection() as connection:
            result = await connection.execute("DELETE FROM orders WHERE id = $1", order_id)
            
            if result == "DELETE 0":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting order: {str(e)}"
        )