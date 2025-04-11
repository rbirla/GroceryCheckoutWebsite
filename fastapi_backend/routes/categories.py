from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models import models

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return [{"id": cat.id, "name": cat.name} for cat in categories]