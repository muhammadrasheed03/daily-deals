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

class ScraperError(Exception):
    def __init__(self, url: str, reason: str):
        self.url = url
        self.reason = reason
        super().__init__(f"Failed to scrape {url}: {reason}")
