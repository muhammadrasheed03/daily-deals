from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name:str
    url:str
    price:float
    original_price:float
    retailer:str
    image_url:Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    url: str
    price: float
    original_price: float
    retailer: str
    image_url: Optional[str] = None
    created_at: datetime

    @property
    def discount_percent(self) -> float:
        return round((1-self.price/self.original_price)*100,2)
    
#fake user model
class User(BaseModel):
    id: int
    username: str
    is_premium: bool

#dependency function
async def get_current_user() -> User:
    #later this will decode a JWT token
    #for now it returns a fake user
    return User(id=1, username="muhammadrasheed03", is_premium=True)



app = FastAPI(
    title="Daily Deals API",
    description="Price tracking and deal aggregation service",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #any origin can call my api, fine for dev, but will make frontend url only for security
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store — replaced by a real DB on day 4
_products: list[ProductResponse] = []
_next_id = 1

#protected route
@app.get("/me")
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return{
        "user": current_user,
        "message": f"Welcome back {current_user.username}"
    }


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}


@app.get("/products", response_model=list[ProductResponse])
async def list_products():
    return _products


@app.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    global _next_id
    new_product = ProductResponse(
        id=_next_id,
        name=product.name,
        url=product.url,
        price=product.price,
        original_price=product.original_price,
        retailer=product.retailer,
        image_url=product.image_url,
        created_at=datetime.now(),
    )
    _products.append(new_product)
    _next_id += 1
    return new_product


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    for p in _products:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")


@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductCreate):
    for i, p in enumerate(_products):
        if p.id == product_id:
            updated = ProductResponse(
                id=product_id,
                name=product.name,
                url=product.url,
                price=product.price,
                original_price=product.original_price,
                retailer=product.retailer,
                image_url=product.image_url,
                created_at=p.created_at,
            )
            _products[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int):
    for i, p in enumerate(_products):
        if p.id == product_id:
            _products.pop(i)
            return
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/deals")
async def get_deals(
    retailer: str | None = None,
    max_price: float | None = None,
    min_discount: float | None = None,
):
    return {
        "filters_applied": {
            "retailer": retailer,
            "max_price": max_price,
            "min_discount": min_discount,
        },
        "deals": []
    }
