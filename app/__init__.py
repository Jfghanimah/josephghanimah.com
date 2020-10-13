import os
from flask import Flask
from flask_mail import Mail

from decouple import config

app = Flask(__name__)
mail = Mail()

class Config:
    SECRET_KEY = config('SECRET_KEY')

    GOOGLE_RECAPTCHA_SECRET_KEY = config('GOOGLE_RECAPTCHA_SECRET_KEY') 

    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config("MAIL_USERNAME")
    MAIL_PASSWORD = config("MAIL_PASSWORD")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)

    from app.main.routes import main
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app