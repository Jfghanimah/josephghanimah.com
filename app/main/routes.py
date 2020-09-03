from flask import (Blueprint, render_template, redirect,
                   url_for, send_from_directory, request, current_app)

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


@main.route("/index")
@main.route("/home")
@main.route("/")
def home():
    return render_template("home.html", posts=posts)