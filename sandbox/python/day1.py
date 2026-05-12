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

#*args variable number of positional arguments
def log_prices(*args: float) -> None:
    for price in args:
        print(f"Recorded price: ${price: .2f}")

log_prices(899.99, 949.99, 879.99)

#**kwargs variable number of keyword arguments
def create_product_filter(**kwargs) -> dict:
    valid_keys = {"retailer", "max_price", "min_discount", "in_stock"}
    return {k: v for k, v in kwargs.items() if k in valid_keys}

filters = create_product_filter(retailer="Amazon", max_price= 500.0, min_discount=20.0)
print(filters)

# both together like a real world pattern

def build_deal_query(endpoint: str, *product_ids: int, **filters) -> str:
    ids = ",".join(str(id) for id in product_ids)
    params = "&".join(f"{k}={v}" for k, v in filters.items())
    return f"{endpoint}?ids={ids}&{params}"

query = build_deal_query("/api/deals", 1, 2, 3, retailer="Amazon", in_stock=True)

# custom exception creation

class ScraperError(Exception):
    def __init__(self, url: str, reason: str):
        self.url = url
        self.reason = reason
        super().__init__(f"Failed to scrape {url}: {reason}")

    
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
#print(history)

print(query)

#implentation using custom exception

def scrape_price(url: str):
    if "blocked" in url:
        raise ScraperError(url, "site blocked request")
    elif "empty" in url:
        raise ScraperError(url, "page returned no content")
    else:
        return 99.99

try:
    price = scrape_price("https://dell.com/xps15")
    print(f"Got price: ${price}")
except ScraperError as e:
    print(f"Scrape failed: {e}")

try:
    price = scrape_price("this website has scraping blocked")
    print(f"Got price: ${price}")
except ScraperError as e:
    print(f"Scrape failed: {e}")

try:
    price = scrape_price("the link returned is empty")
    print(f"Got price: ${price}")
except ScraperError as e:
    print(f"Scrape failed: {e}")
finally:
    print("Scraper session closed")
