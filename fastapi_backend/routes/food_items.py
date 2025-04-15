from fastapi import APIRouter, Depends
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
def get_all_food_items(db: Session = Depends(get_db)):
    items = db.query(models.FoodItem).all()
    return [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "image_url": item.image_url,
            "category": item.category.name if item.category else None
        } for item in items
    ]