import urllib
import json

import pandas as pd
import numpy as np
from datetime import datetime

from flask import (Blueprint, render_template, redirect, flash , url_for, send_from_directory, request, current_app)

from app.main.rating import new_rating

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


@main.route("/")
def home():    
    return render_template("home.html")


@main.route("/about")
def about():
    return render_template("about.html", title="About")



# Projects
@main.route("/lol-draft")
def lol_draft_project():
    return render_template("project1.html", title="Lol Draft Analyzer")

@main.route("/discordbot")
def discord_bot_project():
    return render_template("project2.html", title="Community AI Chatbot")

@main.route("/snake-ai")
def snake_ai_project():
    return render_template("project3.html", title="Snake Game AI")

@main.route("/rating")
def rating_project():
    return render_template("project4.html", title="Improved Glicko2 Rating System")

@main.route("/algo-trading")
def algo_trading_project():
    return render_template("project5.html", title="Algorithmic Trading Bot")


@main.route("/video")
def video():
    return render_template("video.html", video_name="EternalSunshine.mp4", caption_name="EternalSunshine.vtt", title="Video")



@main.route("/smash")
def smash():
    ratings_df = pd.read_csv("elos.csv", index_col=0)
    ratings_df = ratings_df.sort_values(by='Rating', ascending=False)
    ratings_df.index = np.arange(1, len(ratings_df)+1)

    # Add Bootstrap classes to the generated HTML table
    table_html = ratings_df.to_html(classes="table table-striped table-hover align-middle", border=0)

    return render_template("smash.html", table=table_html, title="Smash Ranks")


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

