from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Or your actual DB URI

    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)

    from .routes import routes_bp
    app.register_blueprint(routes_bp)

    return app