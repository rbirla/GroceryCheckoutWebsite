import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.database import SessionLocal
from models.models import Category


def seed_categories():
    db = SessionLocal()
    category_names = ["Fruits", "Vegetables", "Dairy", "Bakery"]
    for name in category_names:
        if not db.query(Category).filter_by(name=name).first():
            db.add(Category(name=name))
    db.commit()
    db.close()


if __name__ == "__main__":
    seed_categories()