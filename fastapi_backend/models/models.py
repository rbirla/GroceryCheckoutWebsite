from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    food_items = relationship("FoodItem", back_populates="category")

class FoodItem(Base):
    __tablename__ = "food_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="food_items")