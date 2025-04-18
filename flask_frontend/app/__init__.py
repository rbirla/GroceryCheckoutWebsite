from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
   
    app = Flask(__name__, instance_relative_config=True)


    app.config['SECRET_KEY'] = 'secretkey123'


    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)


    from .models import User, Product, Card
    migrate = Migrate(app, db)

  
    from .routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
