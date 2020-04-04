from flask import render_template
from repositories import db

#@app.route('/')
def home():
    dbrows = db.getCompetitions()

    return render_template("home.html", dbrows=dbrows)
