import os
from flask import Flask

app = Flask(__name__)

class Config:
    SECRET_KEY = 'd75b6bf0e0aa2561ccf6bb5ee4c4d119'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.main.routes import main
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app