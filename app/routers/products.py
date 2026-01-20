from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.product import Product
from models.user import User
from schemas.product import ProductCreate, Product as ProductSchema
import oauth2
from sqlalchemy import func

router = APIRouter()

@router.post("/products", response_model=ProductSchema)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user) # Get full user object
):
    # 1. Security Check: Are you a seller?
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can add products")

    # 2. Create Product (Assigning owner_id automatically)
    new_product = Product(
        **product.model_dump(),
        owner_id=current_user.id # <--- This links the product to YOU
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/products", response_model=List[ProductSchema])
def read_products(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None, # <--- New Parameter
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    # If user sent ?search=something, filter the query
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
        
    products = query.offset(skip).limit(limit).all()
    return products

# DELETE /products/name/iphone
@router.delete("/products/name/{name}")
def delete_product_by_name(
    name: str, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    # 1. Search for the product (Case Insensitive)
    # ❌ OLD ERROR: db.query(models.Product)...
    # ✅ FIXED: Just use 'Product' directly
    product = db.query(Product).filter(
        func.lower(Product.name) == name.lower()
    ).first()

    # 2. Check if it exists
    if not product:
        raise HTTPException(
            status_code=404, 
            detail=f"Product with name '{name}' not found"
        )

    # 3. Delete it
    db.delete(product)
    db.commit()

    return {"message": f"Product '{product.name}' deleted successfully"}