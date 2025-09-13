from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from datetime import datetime
from app.models.schemas import ProductCreate, ProductUpdate, ProductResponse, HealthCheck
from app.db.mysql import get_mysql_connection

router = APIRouter(prefix="/mysql", tags=["MySQL"])


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check for MySQL"""
    try:
        async with get_mysql_connection() as cursor:
            await cursor.execute("SELECT 1")
            await cursor.fetchone()
        return HealthCheck(
            status="healthy",
            database="MySQL",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MySQL health check failed: {str(e)}"
        )


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """Create a new product in MySQL"""
    try:
        product_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        
        async with get_mysql_connection() as cursor:
            await cursor.execute("""
                INSERT INTO products (id, name, description, price, category, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (product_id, product.name, product.description, product.price, 
                  product.category, created_at, created_at))
            
        return ProductResponse(
            id=product_id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            created_at=created_at,
            updated_at=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating product: {str(e)}"
        )


@router.get("/products", response_model=List[ProductResponse])
async def get_products():
    """Get all products from MySQL"""
    try:
        async with get_mysql_connection() as cursor:
            await cursor.execute("""
                SELECT id, name, description, price, category, created_at, updated_at
                FROM products
                ORDER BY created_at DESC
            """)
            rows = await cursor.fetchall()
            
            products = []
            for row in rows:
                products.append(ProductResponse(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    price=float(row[3]),
                    category=row[4],
                    created_at=row[5],
                    updated_at=row[6]
                ))
            return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching products: {str(e)}"
        )


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get a specific product by ID from MySQL"""
    try:
        async with get_mysql_connection() as cursor:
            await cursor.execute("""
                SELECT id, name, description, price, category, created_at, updated_at
                FROM products WHERE id = %s
            """, (product_id,))
            row = await cursor.fetchone()
            
            if row:
                return ProductResponse(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    price=float(row[3]),
                    category=row[4],
                    created_at=row[5],
                    updated_at=row[6]
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching product: {str(e)}"
        )


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: ProductUpdate):
    """Update a product in MySQL"""
    try:
        update_fields = []
        values = []
        
        # Build dynamic update query
        for field, value in product_update.model_dump().items():
            if value is not None:
                update_fields.append(f"{field} = %s")
                values.append(value)
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
        
        # Add updated_at field
        update_fields.append("updated_at = %s")
        values.append(datetime.utcnow())
        values.append(product_id)
        
        async with get_mysql_connection() as cursor:
            query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = %s"
            await cursor.execute(query, values)
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
            
            # Fetch updated product
            await cursor.execute("""
                SELECT id, name, description, price, category, created_at, updated_at
                FROM products WHERE id = %s
            """, (product_id,))
            row = await cursor.fetchone()
            
            return ProductResponse(
                id=row[0],
                name=row[1],
                description=row[2],
                price=float(row[3]),
                category=row[4],
                created_at=row[5],
                updated_at=row[6]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating product: {str(e)}"
        )


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str):
    """Delete a product from MySQL"""
    try:
        async with get_mysql_connection() as cursor:
            await cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting product: {str(e)}"
        )