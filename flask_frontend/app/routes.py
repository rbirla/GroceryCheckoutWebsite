from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from flask import session, jsonify, request
from app.models import User, Product, Card
from app.forms import RegistrationForm, LoginForm, EditProfileForm, EditPaymentForm, EditAddressForm 
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

   
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    session['cart'] = cart
    session['cart_count'] = sum(cart.values())

    return jsonify(success=True, cart_count=session['cart_count'])



@routes_bp.route('/products')
def products():
    category = request.args.get('category', '').strip()
    ingredient = request.args.get('ingredient', '').strip()
    sort = request.args.get('sort', '').strip()
    search = request.args.get('search', '').strip() 

    params = {}
    if category:
        params["category"] = category
    if ingredient:
        params["ingredient"] = ingredient
    if sort:
        params["sort"] = sort
    if search:
        params["search"] = search  

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
        user = User(username=form.username.data, email=form.email.data)
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

@routes_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    cart = session.get('cart', {})
    product_ids = list(cart.keys())

    try:
     
        response = requests.get("http://localhost:8000/food-items/")
        all_items = response.json()

        
        cart_items = []
        for item in all_items:
            if str(item['id']) in cart:
                cart_items.append({
                    "name": item["name"],
                    "image_url": item["image_url"],
                    "quantity": cart[str(item["id"])]
                })

        return render_template('dashboard.html', cart_items=cart_items)

    except Exception as e:
        print("❌ Failed to fetch dashboard cart items:", e)
        return render_template('dashboard.html', cart_items=[])

@routes_bp.route('/delete-card', methods=['POST'])
@login_required
def delete_card():
    data = request.get_json()
    card_id = data.get('card_id')

    card = Card.query.filter_by(id=card_id, user_id=current_user.id).first()
    if card:
        db.session.delete(card)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 404


@routes_bp.route('/set-default-card', methods=['POST'])
@login_required
def set_default_card():
    data = request.get_json()
    card_id = data.get('card_id')

  
    card = Card.query.filter_by(id=card_id, user_id=current_user.id).first()
    if not card:
        return jsonify(success=False), 404


    Card.query.filter_by(user_id=current_user.id).update({'is_default': False})
    card.is_default = True
    db.session.commit()

    return jsonify(success=True)



@routes_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    personal_form = EditProfileForm(prefix="personal", obj=current_user)
    payment_form = EditPaymentForm(prefix="payment")
    payment_form.card_number.data = ''  # Always clear this field

    address_form = EditAddressForm(prefix="address", obj=current_user)


    if personal_form.validate_on_submit() and 'personal_submit' in request.form:
        current_user.first_name = personal_form.first_name.data
        current_user.last_name = personal_form.last_name.data
        current_user.email = personal_form.email.data
        current_user.age = personal_form.age.data
        current_user.sex = personal_form.sex.data
        db.session.commit()
        flash('✅ Personal Info updated!', 'success')
        return redirect(url_for('routes.edit_profile', tab='personal'))
    
    if request.method == 'POST':
        print("🔁 Form POST received")
        print("✅ Form valid:", payment_form.validate_on_submit())
        print("🧾 Form errors:", payment_form.errors)
        print("🧾 Raw form data:", request.form)
        print("🔐 User ID:", current_user.id)


 
    if request.method == 'POST' and 'payment_submit' in request.form:
        raw_number = request.form.get('payment-card_number', '').replace(" ", "")
        payment_form.card_number.data = raw_number 

        print("✅ Form valid:", payment_form.validate_on_submit())
        print("🧾 Form errors:", payment_form.errors)

    if payment_form.validate_on_submit() and 'payment_submit' in request.form:
        card_number = payment_form.card_number.data.replace(" ", "")
        brand = ""
        logo_url = ""

        if card_number.startswith("4"):
            brand = "visa"
            logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Old_Visa_Logo.svg/250px-Old_Visa_Logo.svg.png"
        elif card_number.startswith("5"):
            brand = "mastercard"
            logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/MasterCard_1979_logo.svg/250px-MasterCard_1979_logo.svg.png"
        elif card_number.startswith("3"):
            brand = "amex"
            logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/American_Express_logo_%282018%29.svg/1200px-American_Express_logo_%282018%29.svg.png"

        
        if payment_form.set_primary.data:
            Card.query.filter_by(user_id=current_user.id).update({'is_default': False})

        new_card = Card(
            user_id=current_user.id,
            last4=card_number[-4:],
            brand=brand,
            logo_url=logo_url,
            is_default=payment_form.set_primary.data
        )
        db.session.add(new_card)
        db.session.commit()

        flash('💳 New card added!', 'success')
        return redirect(url_for('routes.edit_profile', tab='payment'))

    
    if address_form.validate_on_submit() and 'address-submit' in request.form:
        current_user.street = address_form.street.data
        current_user.city = address_form.city.data
        current_user.province = address_form.province.data
        current_user.country = address_form.country.data
        current_user.postal_code = address_form.postal_code.data
        db.session.commit()
        flash('🏠 Address updated!', 'success')
        return redirect(url_for('routes.edit_profile', tab='address'))

   
    saved_cards = Card.query.filter_by(user_id=current_user.id).order_by(Card.is_default.desc()).all()


    return render_template(
        'edit_profile.html',
        personal_form=personal_form,
        payment_form=payment_form,
        address_form=address_form,
        active_tab=request.args.get('tab', 'personal'),
        saved_cards=saved_cards
    )


    






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@routes_bp.route('/update-cart', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))
    change = int(data.get('change'))  

    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id] = max(1, cart[product_id] + change)
        session['cart'] = cart
        session['cart_count'] = sum(cart.values())
        return jsonify(success=True)
    return jsonify(success=False)


@routes_bp.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    product_ids = list(cart.keys())

    try:
        response = requests.get("http://localhost:8000/food-items/")
        all_items = response.json()

        cart_items = []
        for item in all_items:
            if str(item['id']) in cart:
                cart_items.append({
                    "product": item,
                    "quantity": cart[str(item['id'])]
                })

        saved_cards = Card.query.filter_by(user_id=current_user.id).order_by(Card.is_default.desc()).all()

        return render_template('cart.html', cart_items=cart_items, saved_cards=saved_cards, checkout_mode=True)


    except Exception as e:
        print("❌ Failed to fetch cart items:", e)
        return render_template('cart.html', cart_items=[], saved_cards=[])




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

@routes_bp.route('/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))
    cart = session.get('cart', {})

    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        session['cart_count'] = sum(cart.values())
    return jsonify(success=True)

@routes_bp.route('/mock-payment', methods=['GET', 'POST'])
@login_required
def mock_payment():
    if request.method == 'POST':
        current_user.subscribed = True
        db.session.commit()
        flash('You have successfully subscribed to our weekly subscription', 'success')
        return redirect(url_for('routes.dashboard'))
    return render_template('mock_payment.html')

@routes_bp.route('/unsubscribe', methods=['POST'])
@login_required
def unsubscribe():
    current_user.subscribed = False
    db.session.commit()
    flash('You have successfully unsubscribed from our newsletter.', 'info')
    return render_template('dashboard.html', name=current_user.username, subscribed=current_user.subscribed)

@routes_bp.route('/checkout', methods=['GET'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart or sum(cart.values()) == 0:
        flash("❌ You must have at least one item in your cart to proceed to checkout.", "danger")
        return redirect(url_for('routes.cart'))

  
    saved_cards = Card.query.filter_by(user_id=current_user.id).order_by(Card.is_default.desc()).all()

    return render_template(
        'checkout_modal.html',
        saved_cards=saved_cards,
        user=current_user
    )


@routes_bp.route('/process-checkout', methods=['POST'])
@login_required
def process_checkout():
  
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    street = request.form.get('street')
    city = request.form.get('city')
    province = request.form.get('province')
    country = request.form.get('country')
    postal_code = request.form.get('postal_code')
    card_id = request.form.get('selected_card')

  
    selected_card = Card.query.filter_by(id=card_id, user_id=current_user.id).first()
    if not selected_card:
        flash("❌ Invalid card selected.", "danger")
        return redirect(url_for('routes.cart'))

 
    cart = session.get('cart', {})
    if not cart or sum(cart.values()) == 0:
        flash("❌ Your cart is empty. Please add items before checkout.", "warning")
        return redirect(url_for('routes.cart'))

   
    print("✅ Order Summary:")
    print("Name:", first_name, last_name)
    print("Email:", email)
    print("Shipping to:", street, city, province, postal_code, country)
    print("Card used:", selected_card.brand, "••••", selected_card.last4)

  
    session['cart'] = {}
    session['cart_count'] = 0

    flash("🎉 Order placed successfully!", "success")
    return render_template('checkout_success.html')



