from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.order import Order, OrderItem
from models.product import Product
from models.user import User
from schemas.order import OrderCreate, OrderOut as OrderSchema
from typing import List
import oauth2

router = APIRouter()

@router.post("/orders", response_model=OrderSchema)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        # Create initial order
        db_order = Order(user_id=current_user.id, status="pending")
        db.add(db_order)
        db.flush() # Flush to assign an ID to db_order without committing yet

        for item_data in order.items:
            # LOGIC 1: Check if product exists
            product = db.query(Product).filter(Product.id == item_data.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with ID {item_data.product_id} not found")

            # LOGIC 2: Check if enough stock exists
            if product.stock < item_data.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product '{product.name}'. Available: {product.stock}, Requested: {item_data.quantity}")

            # LOGIC 4: DEDUCT the stock
            product.stock -= item_data.quantity
            db.add(product) # Mark product for update

            # LOGIC 3: Create OrderItems
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=product.id,
                quantity=item_data.quantity
            )
            db.add(db_item)

        # If we got here, all items are valid and stock is updated in session
        db.commit()
        db.refresh(db_order)
        return db_order

    except HTTPException as e:
        db.rollback() # Rollback ANY changes (order creation, stock updates) if validation fails
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# GET /orders (Protected)
@router.get("/orders", response_model=List[OrderSchema])
def get_my_orders(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    
    return orders

from schemas.order import SellerSales

# GET /seller/orders
@router.get("/seller/orders", response_model=List[SellerSales])
def get_seller_sales(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can view sales")

    # query OrderItems where product.owner_id == current_user.id
    # We need to join OrderItem -> Product, and OrderItem -> Order -> User (to get buyer name)
    
    results = db.query(
        OrderItem.id,
        Product.name.label("product_name"),
        OrderItem.quantity,
        Order.date,
        User.username.label("buyer_name")
    ).join(Product, OrderItem.product_id == Product.id)\
     .join(Order, OrderItem.order_id == Order.id)\
     .join(User, Order.user_id == User.id)\
     .filter(Product.owner_id == current_user.id)\
     .all()

    return results
