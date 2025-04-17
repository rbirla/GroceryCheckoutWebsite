**Course:** BTP405 – Winter 2025  
**Instructors:** Prof. Eden Burton, Prof. Hina Tariq, Prof. Mazier Sojoudian  
**Due Date:** Week of April 15  
**Team:** Group 9

---

## System Architecture

![Architecture Diagram](docs/architecture.png) 

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




---

## 🛠️ Running the App Locally

```bash
git clone https://github.com/yourgroup/localharvest.git
cd localharvest
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Access the app at: `http://127.0.0.1:5000`

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

## 🔮 Future Work

- Add persistent cart using user database
- Implement real-time stock tracking
- Integrate Stripe for real checkout
- User order history and saved addresses
- Admin dashboard to manage products

---

## 📎 Reference Artifacts
- Architecture diagram (draw.io)
- Product backlog (JIRA or Trello link)
- Code documentation (Python docstrings throughout)

