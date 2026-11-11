# LocalHarvest

A grocery store web app built as a team project at Seneca Polytechnic (2025). Shoppers can browse and filter products, manage a cart, save payment cards and addresses, and go through a mock checkout.

It runs as two services:
- **`fastapi_backend/`** serves the product catalogue as a REST API (FastAPI + SQLAlchemy + SQLite).
- **`flask_frontend/`** is the website itself. It calls the API for product data and handles accounts, the cart and checkout (Flask + Jinja2 + Bootstrap).

## Tech Stack

**Frontend:**
- HTML5 + Bootstrap 5
- Jinja2 templating for dynamic UI rendering

**Backend:**
- Flask with Blueprint routing (`routes.py`)
- Flask-WTF for form handling and validation
- Sessions used for cart storage (per-user)
- FastAPI integration to fetch dynamic product data via REST API

## Database
- **Type:** Relational (SQLAlchemy ORM with SQLite by default)
- **Stored Data:** User profile information (name, age, sex, payment method, address, etc.)
- **Cart:** Session-based, stored per user in Flask session, not persisted in database
- **Product Data:** Pulled dynamically from external FastAPI API (not stored in database)


**Authentication:**
- Flask-Login for user sessions and authorization control

---

## 🔍 Features Overview

- User Registration and Login
- Product Listing Page with:
  - Category, Ingredient, and Sort filters
  - Search functionality with dynamic query string support
- Product Detail Page
  - Expanded product info and "Frequently Bought Together"
- Shopping Cart
  - Add/remove/update quantities
  - Session-based persistence
  - Mock checkout flow
- Tabbed "Edit Profile" UI with sections:
  - Personal Info (Name, Email, Age, Sex)
  - Payment Method (Mock Credit Card)
  - Address (Street, City, Province, Country, Postal Code)

---

## 🛠️ Running the App Locally

You need Python 3.10 or newer (tested on 3.13). The two services run in separate terminals.

**1. Clone the repo**

```bash
git clone https://github.com/rbirla/GroceryCheckoutWebsite.git
cd GroceryCheckoutWebsite
```

**2. Start the product API (terminal 1)**

```bash
cd fastapi_backend
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --port 8000
```

The product catalogue (`localharvest.db`) is included, so the API has data right away. You can check it at `http://127.0.0.1:8000/food-items/`.

**3. Start the website (terminal 2)**

```bash
cd flask_frontend
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env         # macOS/Linux: cp .env.example .env
python run.py
```

Open `http://127.0.0.1:5000`, register an account, and add a card under **Edit Profile → Payment** before checking out. Payments are mocked, so use a test number like `4242 4242 4242 4242`, never a real card.

---

## 🚀 Deployment Strategy

- Can be hosted on PythonAnywhere, Render.com, or Replit
- `.env` file to store config secrets like `SECRET_KEY`
- No hardcoded file paths – all routes are dynamic
- FastAPI backend can be deployed independently

---

## 📅 Sprint Changelog

### Sprint 1 – Week of March 25
- Product filtering with categories/ingredients
- Login and registration working
- Initial layout of dashboard

### Sprint 2 – Week of April 1
- Cart logic (add, update, delete) complete
- Integrated FastAPI endpoint for product listings
- Product detail and related products section

### Sprint 3 – Week of April 8
- Tab-based Edit Profile form implemented
- Flask-WTF form with validation
- Connected dynamic data to dashboard

---



