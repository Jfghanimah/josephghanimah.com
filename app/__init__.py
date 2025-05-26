import os
from flask import Flask

from decouple import config

app = Flask(__name__)

class Config:
    SECRET_KEY = config('SECRET_KEY')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    from app.main.routes import main
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app