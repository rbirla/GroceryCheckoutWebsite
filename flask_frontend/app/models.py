from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.schema import UniqueConstraint

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(120), nullable=False)  # no unique=True here
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    payment_method = db.Column(db.String(100))  # imaginary credit card
    street = db.Column(db.String(150))
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    subscribed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(150), nullable=False)

    __table_args__ = (
        UniqueConstraint('email', name='uq_user_email'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
