from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.product import Product
from schemas.product import ProductCreate, Product as ProductSchema

router = APIRouter()

@router.post("/products", response_model=ProductSchema)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    # Helper to convert pydantic model to dict
    product_data = product.model_dump()
    db_product = Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

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