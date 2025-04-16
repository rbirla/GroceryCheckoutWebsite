from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from flask import session, jsonify, request
from app.models import User, Product
from app.forms import RegistrationForm, LoginForm
from app import login_manager, db
import requests
import random

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('index.html')
@routes_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if not current_user.is_authenticated:
        return jsonify(success=False, message="You must be logged in to add to cart.")

    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify(success=False, message="Missing product ID")

    cart = session.get('cart', {})
    product_id_str = str(product_id)

    # Increment quantity or add new product
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    session['cart'] = cart
    session['cart_count'] = sum(cart.values())

    return jsonify(success=True, cart_count=session['cart_count'])



@routes_bp.route('/products')
def products():
    category = request.args.get('category', '').strip()
    ingredient = request.args.get('ingredient', '').strip()
    sort = request.args.get('sort', '').strip()
    search = request.args.get('search', '').strip()  # <-- NEW

    params = {}
    if category:
        params["category"] = category
    if ingredient:
        params["ingredient"] = ingredient
    if sort:
        params["sort"] = sort
    if search:
        params["search"] = search  # <-- Pass it to FastAPI

    try:
        response = requests.get("http://localhost:8000/food-items/", params=params)
        items = response.json()

        categories = sorted({item["category"] for item in items if item.get("category")})
        ingredients = sorted({ing for item in items for ing in item.get("ingredients", [])})

    except Exception as e:
        print("❌ Failed to fetch items from API:", e)
        items = []
        categories = []
        ingredients = []

    return render_template(
        'products.html',
        items=items,
        categories=categories,
        ingredients=ingredients
    )


@routes_bp.route('/about')
def about():
    return render_template('about.html')

@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@routes_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@routes_bp.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.query.filter(Product.id.in_(product_ids)).all()

    cart_items = []
    for product in products:
        quantity = cart[str(product.id)]
        cart_items.append({"product": product, "quantity": quantity})

    return render_template('cart.html', cart_items=cart_items)


@routes_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    try:
        response = requests.get("http://localhost:8000/food-items/")
        items = response.json()

        product = next((item for item in items if item["id"] == product_id), None)
        if not product:
            return "Product not found", 404

        same_category = [item for item in items if item["category"] == product["category"] and item["id"] != product["id"]]
        random.shuffle(same_category)
        related_items = same_category[:5]

        return render_template("product_detail.html", product=product, related_items=related_items)

    except Exception as e:
        print("❌ Failed to fetch product:", e)
        return "Error loading product", 500

@routes_bp.route('/mock-payment')
@login_required
def mock_payment():
    return render_template('mock_payment.html')