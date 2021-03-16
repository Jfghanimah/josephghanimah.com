import urllib
import json

from datetime import datetime

from flask import (Blueprint, render_template, redirect, flash ,
                   url_for, send_from_directory, request, current_app)

from flask_mail import Message

from app.main.forms import ContactForm
from app import mail

main = Blueprint('main', __name__)


# this STS is to for HTTPS connections
@main.after_request
def apply_caching(response):
    response.headers["Strict-Transport-Security"] = 'max-age=63072000; includeSubDomains; preload'
    response.headers
    return response


@main.route('/robots.txt')
@main.route('/sitemap.xml')
@main.route('/favicon.ico')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


@main.route("/index")
@main.route("/home")
@main.route("/main")
def redirect_home():
    return redirect(url_for('main.home'))


@main.route("/", methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        if verify_reCAPTCHA():
            form_answer = request.form['question']
            correct_answer = datetime.today().day
            if not (form_answer == str(correct_answer)):
                print(form_answer, correct_answer)
                flash("Your response to the math question is wrong!", "red")
            else:
                name = form.name.data
                email = form.email.data
                subject = form.subject.data
                body = form.message.data
                send_email(name=name, subject=subject, email=email, body=body, answer=form_answer)
                flash("Your message has been sent!", "green")
                return redirect(url_for("main.home")) #This resets the page entirely 
        else:
            flash("Invalid reCAPTCHA. Please try again.", "red")
    
    if form.email.errors:
        flash(f"There was an error with your information: {', '.join(form.email.errors)}", "red")
    
    return render_template("home.html", form=form)


def send_email(name, email, subject, body, answer):
    msg = Message(subject, sender=("Josephghanimah.com","jfghanimah@gmail.com"))
    msg.recipients=["jfghanimah@gmail.com"]
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {body}\nAnswer: {answer}"
    mail.send(msg)


# Returns True or False depending on the google recaptcha api call
def verify_reCAPTCHA():
    recaptcha_response = request.form.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': current_app.config['GOOGLE_RECAPTCHA_SECRET_KEY'],
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result['success']