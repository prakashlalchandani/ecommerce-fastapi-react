from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
    image_url: str = "https://via.placeholder.com/150"

from schemas.user import User # Import User schema

class Product(ProductCreate):
    id: int
    owner_id: int
    owner: User # Nested user object to get username

    class Config:
        from_attributes = True