from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

#this class defines the 'products' table in PostgreSQL
#every attribute with Column becomes a column in the table
class Product(Base):
    #tells SQLAlchemy the actual table name in the database
    __tablename__= "products"

    #primary key - unique identifier for each row
    #autoincrement=True means the DB assigns this automatically
    id = Column(Integer, primary_key=True, autoincrement=True)

    #String (255) means max 255 characters
    #nullable=False means this column is required - can't be empty
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    retailer = Column(String(100), nullable=False)

    #Float for decimal numbers like prices
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=False)

    #nullable=True means optional - not every product has an image
    image_url = Column(String(500), nullable=True)

    # boolean with a default value
    in_stock = Column(Boolean, default=True)

    #DateTime - automatically set to now when a product is created
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    #relationship - tells SQLAlchemy that one Product has many PriceHistory records
    #"PriceHistory" refers to the class below
    #back_populates creates the reverse link so PriceHistory can access its Product
    price_history = relationship("PriceHistory", back_populates="product")

    def discount_percent(self) -> float:
        if self.original_price == 0:
            return 0.0
        return round((1-self.price/self.original_price)*100, 2)
    
    def __repr__(self) ->str:
        return f"Product(id={self.id}, name={self.name}, price={self.price})"
    

#this class defines the 'price_history' table
#every time a product's price changes, a new row gets added here
class PriceHistory(Base):
    __tablename__ = "price_history"

    id= Column(Integer, primary_key=True, autoincrement=True)

    #ForeignKey links this table to the products table
    #"products.id" means this column references the id column in products
    #when i delete a product, what happens to its price history?
    #to answer, ondelete="CASCADE" means delete the history records too automatically
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    #the price at this point in time
    recorded_price = Column(Float, nullable=False)

    #when this price was recorded
    recorded_at = Column(DateTime, default=datetime.now)

    #the reverse side of the relationship defined in Product
    product = relationship("Product", back_populates="price_history")

    def __repr__(self) -> str:
        return f"PriceHistory(product_id={self.product_id}, price={self.recorded_price})"