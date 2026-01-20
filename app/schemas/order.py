from pydantic import BaseModel
from typing import List

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemSchema]

# 1. New Output Schema for Items inside the order response
class OrderItemOut(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

# 2. Upgraded Order Response Schema
class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    items: List[OrderItemOut] = []  # <--- THE KEY CHANGE: Show the list of items!

    class Config:
        from_attributes = True

# 3. Seller Sales Tracker Schema
from datetime import datetime
class SellerSales(BaseModel):
    id: int
    buyer_name: str
    product_name: str
    quantity: int
    date: datetime

    class Config:
        from_attributes = True