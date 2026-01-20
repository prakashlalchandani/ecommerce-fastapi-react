import sys
import os
from passlib.context import CryptContext

# 1. Setup path to find the 'app' folder
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from database import SessionLocal
from models.product import Product
from models.user import User
from models.order import Order, OrderItem

# Password Hashing Tool
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. The Data List (30 Items)
products_data = [
    # --- Electronics ---
    {"name": "Gaming Laptop", "description": "High performance gaming laptop with RTX 4060", "price": 1200.99, "stock": 5, "image_url": "https://dummyimage.com/400x400/2c3e50/ffffff&text=Gaming+Laptop"},
    {"name": "Wireless Headphones", "description": "Noise cancelling over-ear headphones", "price": 199.50, "stock": 15, "image_url": "https://dummyimage.com/400x400/2c3e50/ffffff&text=Headphones"},
    {"name": "4K Monitor", "description": "27-inch IPS display for creators", "price": 350.00, "stock": 8, "image_url": "https://dummyimage.com/400x400/2c3e50/ffffff&text=4K+Monitor"},
    {"name": "Mechanical Keyboard", "description": "RGB backlit tactile switches", "price": 89.99, "stock": 20, "image_url": "https://dummyimage.com/400x400/2c3e50/ffffff&text=Keyboard"},
    {"name": "Gaming Mouse", "description": "Lightweight wireless mouse", "price": 49.99, "stock": 25, "image_url": "https://dummyimage.com/400x400/2c3e50/ffffff&text=Mouse"},
    {"name": "DSLR Camera", "description": "Professional camera with 18-55mm lens", "price": 650.00, "stock": 3, "image_url": "https://dummyimage.com/400x400/2c3e50/ffffff&text=Camera"},
    {"name": "Bluetooth Speaker", "description": "Portable waterproof speaker", "price": 35.00, "stock": 30, "image_url": "https://dummyimage.com/400x400/2c3e50/ffffff&text=Speaker"},

    # --- Clothes ---
    {"name": "Cotton T-Shirt", "description": "100% organic cotton basic tee", "price": 15.00, "stock": 50, "image_url": "https://dummyimage.com/400x400/e74c3c/ffffff&text=T-Shirt"},
    {"name": "Denim Jeans", "description": "Slim fit blue jeans", "price": 45.00, "stock": 40, "image_url": "https://dummyimage.com/400x400/e74c3c/ffffff&text=Jeans"},
    {"name": "Winter Jacket", "description": "Insulated jacket for cold weather", "price": 120.00, "stock": 10, "image_url": "https://dummyimage.com/400x400/e74c3c/ffffff&text=Jacket"},
    {"name": "Running Sneakers", "description": "Lightweight running shoes", "price": 85.00, "stock": 20, "image_url": "https://dummyimage.com/400x400/e74c3c/ffffff&text=Sneakers"},
    {"name": "Hoodie", "description": "Cozy fleece hoodie", "price": 35.00, "stock": 35, "image_url": "https://dummyimage.com/400x400/e74c3c/ffffff&text=Hoodie"},
    {"name": "Baseball Cap", "description": "Adjustable sports cap", "price": 12.00, "stock": 60, "image_url": "https://dummyimage.com/400x400/e74c3c/ffffff&text=Cap"},
    {"name": "Scarf", "description": "Wool winter scarf", "price": 18.00, "stock": 25, "image_url": "https://dummyimage.com/400x400/e74c3c/ffffff&text=Scarf"},
    {"name": "Summer Dress", "description": "Floral pattern light dress", "price": 55.00, "stock": 15, "image_url": "https://dummyimage.com/400x400/e74c3c/ffffff&text=Dress"},

    # --- Smart Devices ---
    {"name": "Smart Watch", "description": "Fitness tracker with heart rate monitor", "price": 150.00, "stock": 12, "image_url": "https://dummyimage.com/400x400/8e44ad/ffffff&text=Smart+Watch"},
    {"name": "Smart Bulb", "description": "WiFi enabled RGB bulb", "price": 12.99, "stock": 100, "image_url": "https://dummyimage.com/400x400/8e44ad/ffffff&text=Smart+Bulb"},
    {"name": "Smart Plug", "description": "Control appliances from your phone", "price": 15.99, "stock": 80, "image_url": "https://dummyimage.com/400x400/8e44ad/ffffff&text=Smart+Plug"},
    {"name": "Thermostat", "description": "Programmable home thermostat", "price": 199.00, "stock": 5, "image_url": "https://dummyimage.com/400x400/8e44ad/ffffff&text=Thermostat"},
    {"name": "Video Doorbell", "description": "HD security camera doorbell", "price": 99.00, "stock": 10, "image_url": "https://dummyimage.com/400x400/8e44ad/ffffff&text=Doorbell"},
    {"name": "Smart Speaker", "description": "Voice assistant speaker", "price": 49.00, "stock": 20, "image_url": "https://dummyimage.com/400x400/8e44ad/ffffff&text=Voice+Assistant"},
    {"name": "Drone", "description": "Camera drone with 4K video", "price": 450.00, "stock": 2, "image_url": "https://dummyimage.com/400x400/8e44ad/ffffff&text=Drone"},

    # --- Grocery ---
    {"name": "Basmati Rice", "description": "Premium long grain rice (5kg)", "price": 15.00, "stock": 50, "image_url": "https://dummyimage.com/400x400/27ae60/ffffff&text=Rice"},
    {"name": "Almond Milk", "description": "Organic unsweetened milk", "price": 4.50, "stock": 40, "image_url": "https://dummyimage.com/400x400/27ae60/ffffff&text=Milk"},
    {"name": "Arabica Coffee", "description": "Roasted coffee beans (1kg)", "price": 18.00, "stock": 25, "image_url": "https://dummyimage.com/400x400/27ae60/ffffff&text=Coffee"},
    {"name": "Organic Apples", "description": "Fresh red apples (1kg)", "price": 3.00, "stock": 60, "image_url": "https://dummyimage.com/400x400/27ae60/ffffff&text=Apples"},
    {"name": "Bananas", "description": "Fresh bananas (1 bunch)", "price": 1.50, "stock": 100, "image_url": "https://dummyimage.com/400x400/27ae60/ffffff&text=Bananas"},
    {"name": "Whole Wheat Bread", "description": "Freshly baked loaf", "price": 2.50, "stock": 15, "image_url": "https://dummyimage.com/400x400/27ae60/ffffff&text=Bread"},
    {"name": "Free Range Eggs", "description": "Dozen large eggs", "price": 5.00, "stock": 30, "image_url": "https://dummyimage.com/400x400/27ae60/ffffff&text=Eggs"},
    {"name": "Dark Chocolate", "description": "70% cocoa chocolate bar", "price": 3.50, "stock": 80, "image_url": "https://dummyimage.com/400x400/27ae60/ffffff&text=Chocolate"},
]

def seed_database():
    db = SessionLocal()
    try:
        print("[*] Cleaning up old data...")
        # 1. Clear old data
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(Product).delete()
        db.query(User).delete()
        db.commit()

        # 2. Create a "Master Seller"
        hashed_password = pwd_context.hash("12345")
        master_seller = User(username="admin_seller", email="admin@example.com", password=hashed_password, role="seller")
        db.add(master_seller)
        db.commit()
        db.refresh(master_seller) # Get the ID

        print(f"[+] Created Master Seller (ID: {master_seller.id})")

        # 3. Add Products (Linked to Master Seller)
        print("[*] Seeding products...")
        for item in products_data:
            # linking to master_seller.id is the key part!
            product = Product(**item, owner_id=master_seller.id) 
            db.add(product)
        
        db.commit()
        print(f"[+] Successfully added {len(products_data)} products linked to 'admin_seller'!")
        
    except Exception as e:
        db.rollback()
        print(f"[!] Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()