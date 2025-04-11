from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import create_db_and_tables
from routes import categories, food_items

app = FastAPI()

# Allow requests from Flask frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    create_db_and_tables()

app.include_router(categories.router)
app.include_router(food_items.router)