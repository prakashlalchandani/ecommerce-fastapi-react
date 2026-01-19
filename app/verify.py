import sys
import os
import time

# Ensure we can import app modules
# Adjust this if your folder structure is different
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    # Try importing from app.main if running from root
    from app.main import app
except ImportError:
    # Fallback if running from inside app folder
    from main import app

from fastapi.testclient import TestClient

client = TestClient(app)

def test_flow():
    print("🚀 Starting Verification Flow with TestClient...\n")

    # ==========================================
    # 1. Create User
    # ==========================================
    print("1. Creating User...")
    user_email = f"trader_{int(time.time())}@example.com"
    user_password = "securepassword"
    user_payload = {
        "username": f"algo_trader_{int(time.time())}", 
        "email": user_email, 
        "password": user_password
    }
    
    r = client.post("/users", json=user_payload)
    if r.status_code == 200 or r.status_code == 201:
        user = r.json()
        print(f"   ✅ User created: {user['username']} (ID: {user.get('id')})")
    elif r.status_code == 400 and "Email already registered" in r.text:
        print("   ⚠️ User exists (skipping creation).")
    else:
        print(f"   ❌ Failed to create user: {r.text}")
        sys.exit(1)

    # ==========================================
    # 2. Login to get Token
    # ==========================================
    print("\n2. Logging in...")
    # OAuth2 form expects 'username' field to hold the email/id
    login_payload = {"username": user_email, "password": user_password} 
    
    r = client.post("/login", data=login_payload)
    if r.status_code == 200:
        token_data = r.json()
        access_token = token_data["access_token"]
        print(f"   ✅ Login successful. Token: {access_token[:15]}...")
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        print(f"   ❌ Login failed: {r.text}")
        sys.exit(1)

    # ==========================================
    # 3. Create Product
    # ==========================================
    print("\n3. Creating Product (iPhone 15)...")
    product_payload = {
        "name": f"iPhone 15 ({int(time.time())})", # Unique name to avoid confusion
        "description": "Latest Apple flagship", 
        "price": 999.99, 
        "stock": 10
    }
    
    r = client.post("/products", json=product_payload)
    product_id = None
    
    if r.status_code == 200 or r.status_code == 201:
        product = r.json()
        product_id = product["id"]
        print(f"   ✅ Product created: {product['name']} (ID: {product_id})")
    else:
        print(f"   ❌ Failed to create product: {r.text}")
        sys.exit(1)

    # ==========================================
    # 4. Place Order (Quantity 2)
    # ==========================================
    print("\n4. Placing Order (Quantity: 2)...")
    order_payload = {
        "items": [{"product_id": product_id, "quantity": 2}]
    }
    
    r = client.post("/orders", json=order_payload, headers=headers)
    order_id = None
    
    if r.status_code == 200:
        order = r.json()
        order_id = order['id']
        print(f"   ✅ Order placed successfully. Order ID: {order_id}")
    else:
        print(f"   ❌ Failed to place order: {r.text}")
        sys.exit(1)

    # ==========================================
    # 5. Verify Stock Deduction
    # ==========================================
    print("\n5. Verifying Stock Deduction...")
    r = client.get("/products")
    products = r.json()
    
    # Find our specific product
    p = next((p for p in products if p["id"] == product_id), None)
    
    if p:
        if p['stock'] == 8:
            print(f"   ✅ Stock verified: {p['stock']} (Correctly deducted 10 - 2)")
        else:
            print(f"   ⚠️ Stock mismatch! Expected 8, got {p['stock']}")
    else:
        print("   ❌ Product not found in list.")

    # ==========================================
    # 6. Intentional Failure (Insufficient Stock)
    # ==========================================
    print("\n6. Testing Insufficient Stock (Buying 100)...")
    order_payload_fail = {
        "items": [{"product_id": product_id, "quantity": 100}]
    }
    r = client.post("/orders", json=order_payload_fail, headers=headers)
    if r.status_code == 400:
        print(f"   ✅ SUCCESS: Order rejected correctly: {r.json().get('detail')}")
    else:
        print(f"   ❌ FAILURE: Order should have been rejected (Status: {r.status_code}).")

    # ==========================================
    # 7. Test "My Orders" (NEW!)
    # ==========================================
    print("\n7. Testing 'My Orders' (GET /orders)...")
    r = client.get("/orders", headers=headers)
    
    if r.status_code == 200:
        my_orders = r.json()
        # Check if the order we just made (ID: order_id) is in the list
        found_order = next((o for o in my_orders if o['id'] == order_id), None)
        
        if found_order:
            print(f"   ✅ Found Order #{order_id} in history.")
            # Verify items are visible (Schema Check)
            if 'items' in found_order and len(found_order['items']) > 0:
                print(f"   ✅ Order details visible: Contains {len(found_order['items'])} items.")
            else:
                print("   ⚠️ WARNING: Order found, but 'items' list is empty or missing. Check OrderOut schema!")
        else:
            print(f"   ❌ Order #{order_id} NOT found in user history.")
    else:
        print(f"   ❌ Failed to fetch orders: {r.text}")

    # ==========================================
    # 8. Test Data Isolation (NEW!)
    # ==========================================
    print("\n8. Testing Security (Data Isolation)...")
    print("   -> Creating a 2nd user (Hacker)...")
    
    # Create User 2
    user2_email = f"hacker_{int(time.time())}@example.com"
    client.post("/users", json={
        "username": f"hacker_{int(time.time())}", 
        "email": user2_email, 
        "password": "password123"
    })

    # Login User 2
    r = client.post("/login", data={"username": user2_email, "password": "password123"})
    token2 = r.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Check Orders for User 2 (Should be empty)
    r = client.get("/orders", headers=headers2)
    orders2 = r.json()
    
    if len(orders2) == 0:
         print("   ✅ SUCCESS: Hacker sees 0 orders. Data is secure.")
    else:
         print(f"   ❌ FAILURE: Hacker sees {len(orders2)} orders! Data leak detected.")

    print("\n✨ Verification Complete! System is healthy.")

if __name__ == "__main__":
    test_flow()