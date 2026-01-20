# app/models/product.py

# 👇 ADD "ForeignKey" to this list
from sqlalchemy import Column, Integer, String, Float, ForeignKey 
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    image_url = Column(String, nullable=True)
    
    # Now this will work because we imported it!
    owner_id = Column(Integer, ForeignKey("users.id")) 
    
    owner = relationship("User")