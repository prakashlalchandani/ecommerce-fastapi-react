from fastapi import FastAPI
from database import engine, Base
from routers import users, products, orders, auth
from fastapi.middleware.cors import CORSMiddleware

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API")

# 2. Add the Middleware (The "Unlock" Code)
# This allows ANY website (*) to talk to your backend. 
# In production, you would change ["*"] to ["http://my-frontend.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

# Include routers
app.include_router(users.router, tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(orders.router, tags=["orders"])
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to E-Commerce API. Visit /docs for Swagger UI."}
