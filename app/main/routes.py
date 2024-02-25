import urllib
import json

import pandas as pd
import numpy as np
from datetime import datetime

from flask import (Blueprint, render_template, redirect, flash ,
                   url_for, send_from_directory, request, current_app)

from flask_mail import Message

from app.main.forms import ContactForm
from app.main.rating import new_rating
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


@main.route("/about")
def about():
    return render_template("about.html", title="About")



# Projects
@main.route("/lol-draft")
def lol_draft_project():
    return render_template("project1.html", title="Lol Draft Analyzer")

@main.route("/dcgan")
def dcgan_project():
    return render_template("project2.html", title="Deep Convolutional Generative Adversarial Network")

@main.route("/snake-ai")
def snake_ai_project():
    return render_template("project3.html", title="Snake Game AI")

@main.route("/rating")
def rating_project():
    return render_template("project4.html", title="Improved Glicko2 Rating System")

@main.route("/lifting-app")
def lifting_app_project():
    return render_template("project5.html", title="Social Weight Lifting App")


@main.route("/video")
def video():
    return render_template("video.html", video_name="EternalSunshine.mp4", caption_name="EternalSunshine.vtt", title="Video")


@main.route("/smash")
def smash():
    ratings_df = pd.read_csv("elos.csv", index_col=0)
    ratings_df = ratings_df.sort_values(by='Rating', ascending=False)
    ratings_df.index = np.arange(1, len(ratings_df)+1)

    return render_template("smash.html", table=ratings_df.to_html(), title="Smash Ranks")


@main.route("/smash2",  methods=['GET', 'POST'])
def smash2():
    df = pd.read_csv("elos.csv", index_col=0)
    df = df.sort_values(by='Rating', ascending=False)    
    df.index = np.arange(1, len(df)+1)
    table = df.to_html() 

    df = df.sort_values(by=['Name', 'Rating'], ascending=[True, False])   
    df.index = np.arange(1, len(df)+1)

    choices = []
    for idx, row in df.iterrows():
        choices.append(row)

    if request.method == "POST":
        p1 = int(request.form['player1'])
        p2 = int(request.form['player2'])

        if p1 == p2:
            flash("You selected the same player twice!", "red")
            return redirect(url_for("main.smash2"))
        
        r1 = df.loc[p1].Rating
        c1 = df.loc[p1].Confidence
        r2 = df.loc[p2].Rating
        c2 = df.loc[p2].Confidence

        p1_ratings = new_rating(r1, c1, r2, c2, 1)
        p2_ratings = new_rating(r2, c2, r1, c1, 0)

        # reassign new ratings
        df.at[p1, 'Rating'] = p1_ratings[0]
        df.at[p1, 'Confidence'] = p1_ratings[1]
        df.at[p2, 'Rating'] = p2_ratings[0]
        df.at[p2, 'Confidence'] = p2_ratings[1]

        df.to_csv("elos.csv")

        msg = f"""
        Updated!
        Winner: {df.loc[p1].Name}: {p1_ratings[0]-r1}
        Loser: {df.loc[p2].Name}: {p2_ratings[0]-r2}
        """

        flash(msg, "green")        
        return redirect(url_for("main.smash2"))

    return render_template("smash2.html", table=table, choices=choices)


@main.route("/resume")
def redirect_resume():
    return redirect("https://josephghanimah.com/static/JosephResume.pdf")


@main.route("/github")
def redirect_github():
    return redirect("https://github.com/Jfghanimah")


@main.route("/linkedin")
def redirect_linkedin():
    return redirect("https://www.linkedin.com/in/joseph-ghanimah/")


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




