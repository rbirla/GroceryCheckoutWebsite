
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
def get_all_food_items(
    category: str = Query(None),
    ingredient: str = Query(None),
    sort: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.FoodItem).join(models.Category)
    all_items = query.all()

    
    if category:
        all_items = [item for item in all_items if item.category and item.category.name.lower() == category.lower()]

  
    if ingredient:
        all_items = [
            item for item in all_items 
            if any(ingredient.lower() in ing.lower() for ing in (item.ingredients or "").split(", "))
        ]

   
    if search:
        search = search.strip().lower()
        print(f"\n🔍 Normalized search: '{search}'")

        results = []
        for item in all_items:
            name = item.name.lower()
            cat_name = item.category.name.lower() if item.category else ""
            desc = (item.description or "").lower()
            ingredients_list = item.ingredients.split(", ") if item.ingredients else []
            ingredients = " ".join(ingredients_list).lower()

            score = 0
            if name == search:
                score += 1000
            elif cat_name == search:
                score += 900
            elif search in name:
                score += 700
            elif search in cat_name:
                score += 600
            if search in ingredients:
                score += 300
            if search in desc:
                score += 100

            if score > 0:
                print(f"✅ Match: {item.name} | Score: {score}")
                results.append((score, item))

        results.sort(key=lambda x: (-x[0], x[1].name))  
        items = [item for _, item in results]
    else:
        items = all_items

   
    if sort == "alphabetical":
        items.sort(key=lambda x: x.name.lower())
    elif sort == "price_asc":
        items.sort(key=lambda x: float(x.price))
    elif sort == "price_desc":
        items.sort(key=lambda x: float(x.price), reverse=True)


    return [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "image_url": item.image_url,
            "description": item.description,
            "ingredients": item.ingredients.split(", ") if item.ingredients else [],
            "category": item.category.name if item.category else None
        }
        for item in items
    ] 