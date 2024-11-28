# app/__init__.py
from flask import Flask
from flask_session import Session
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    Session(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app