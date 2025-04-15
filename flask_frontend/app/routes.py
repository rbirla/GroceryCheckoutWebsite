from flask import render_template, redirect, url_for, flash, request, Blueprint, render_template
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Product
from app.forms import RegistrationForm, LoginForm
from app import login_manager, db
import requests

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/products')
def products():
    category = request.args.get('category')
    try:
        params = {"category": category} if category else {}
        response = requests.get("http://localhost:8000/food-items/", params=params)
        items = response.json()
    except Exception as e:
        print("Failed to fetch items from API:", e)
        items = []
    return render_template('products.html', items=items)

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

@routes_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    try:
        response = requests.get(f"http://localhost:8000/food-items/{product_id}")
        product = response.json()
    except Exception as e:
        print("Failed to fetch product:", e)
        product = None
    return render_template('product_detail.html', product=product)
