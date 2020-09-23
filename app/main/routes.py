import urllib
import json

from flask import (Blueprint, render_template, redirect, flash ,
                   url_for, send_from_directory, request, current_app)

from app.main.forms import ContactForm

main = Blueprint('main', __name__)

# this is just a test list
posts = [
    {
        "id" : 1,
        "author": 'Joseph Ghanimah',
        "type": 'blog',
        "title": 'Looking For Writers!',
        "content": """It is a long established fact that a reader will be distracted 
        by the readable content of a page when looking at its layout. 
        """,
        "date_posted": 'April 20, 2018',
        "image": 'static/images/blog.webp'
    },
    {
        "id" : 2,
        "author": 'Joseph Ghanimah',
        "type": 'blog',
        "title": 'Black Ops 4: Release Date!',
        "content": """It is a long established fact that a reader will be distracted 
        by the readable content of a page when looking at its layout. 
        """,
        "date_posted": 'April 21, 2018',
        "image": 'static/images/bo4.webp'
    },
    {
        "id" : 3,
        "author": 'Joseph Ghanimah',
        "type": 'image',
        "title": 'Week 3 Tournament',
        "content": """It is a long established fact that a reader will be distracted 
        by the readable content of a page when looking at its layout. 
        """,
        "date_posted": 'April 23, 2018',
        "image": 'static/images/g3cw3.webp'
    }
]

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
            print(form.name)
            print(form.subject)
            print(form.email)
            print(form.message)
            flash("Your message has been sent!", "green")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid reCAPTCHA. Please try again.", "red")
            return redirect(url_for("main.home"))
    
    return render_template("home.html", posts=posts, form=form)


def send_email():
    return


# Returns True or False depending on the google recaptcha api call
def verify_reCAPTCHA():
    recaptcha_response = request.form.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': '6LdBZM8ZAAAAAPf-wUqbv4btign4HerBSqX4ZM7Q',
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result['success']