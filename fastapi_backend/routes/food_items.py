from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models import models

router = APIRouter(prefix="/food-items", tags=["Food Items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_food_items(category: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.FoodItem)

    if category:
        category = category.strip().capitalize()
        query = query.join(models.Category).filter(models.Category.name == category)

    items = query.all()
    return [
    {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "image_url": item.image_url,
        "description": item.description,
        "ingredients": item.ingredients.split(", ") if item.ingredients else [],
        "category": item.category.name if item.category else None
    } for item in items
]
