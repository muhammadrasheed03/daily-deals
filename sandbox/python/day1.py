from dataclasses import dataclass, field
from typing import Optional 
from datetime import datetime

@dataclass
class Product:
    name: str
    url: str
    price: float
    original_price: float
    retailer: str
    scraped_at: datetime = field(default_factory=datetime.now)
    image_url: Optional[str] = None
    in_stock: bool = True

    def discount_percent(self) -> float:
        if self.original_price == 0:
            return 0.0
        return round((1-self.price/self.original_price)*100, 2)
    
    def is_good_deal(self, threshold: float = 20.0) -> bool:
        return self.discount_percent() >=threshold

@dataclass
class Deal:
    product: Product
    deal_url: str
    expires_at: Optional[datetime] = None
    description: Optional[str] = None

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now()>self.expires_at

@dataclass
class PriceHistory:
    product: Product
    recorded_price: float
    recorded_time: datetime = field(default_factory=datetime.now)
    
#--- excersises ---

#creating a product and printing it
laptop = Product(
    name = "Dell XPS 15",
    url = "https://dell.com/xps15",
    price=899.99,
    original_price = 1199.99,
    retailer= "Dell"
)

print(laptop)
print(f"Discount: {laptop.discount_percent()}%")
print(f"Good deal: {laptop.is_good_deal()}")

#list comprehension, filter products that are good deals

products: list[Product] = [
    laptop,
    Product("USB Cable", "https://amazon.com/cable", 8.99, 9.99, "Amazon"),
    Product("Sony Headphones", "https://sony.com/wh1000", 279.99, 399.99, "Sony")
]

good_deals = [p for p in products if p.is_good_deal()]
print(f"\nGood deals: {[p.name for p in good_deals]}")

#price lookup by product name
price_lookup: dict[str, float] = {p.name: p.price for p in products}
print(f"\nPrice lookup: {price_lookup}")

# f-string formatting
for p in products:
    print(f"{p.retailer:<12} | {p.name:<25} | {p.price:>8.2f} | {p.discount_percent():>5.1f}% off")

#price history
history = PriceHistory(product=laptop, recorded_price=949.99)
print(history)