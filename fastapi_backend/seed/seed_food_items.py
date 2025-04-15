import json
import os
from db.database import SessionLocal
from models.models import FoodItem, Category

def seed_food_items():
    db = SessionLocal()


    file_path = os.path.join(os.path.dirname(__file__), "../data/food_items.json")
    with open(file_path, "r") as file:
        items = json.load(file)

    for item in items:
        category = db.query(Category).filter_by(name=item["category"]).first()
        if category:
            exists = db.query(FoodItem).filter_by(name=item["name"]).first()
            if not exists:
                db.add(FoodItem(
                    name=item["name"],
                    price=item["price"],
                    category_id=category.id,
                    image_url=item["image_url"],
                ))

    db.commit()
    db.close()
    print("Seeded food items from JSON.")

if __name__ == "__main__":
    seed_food_items()