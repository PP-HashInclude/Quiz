from flask import render_template, request, make_response, redirect, url_for, session
from repositories import db
from werkzeug.security import generate_password_hash

#@app.route('/signup')
def signup():
    dbrows = db.getCompetitions()
    competition = request.args.get("competition")
    return render_template("registration.html", competitionselected=competition, registrationmessage="", dbrows=dbrows)

#@app.route('/senddetails')
def register():
    competition = request.form.get('competition')
    name = request.form.get('uname')
    email = request.form.get('email')
    passwd = generate_password_hash(request.form.get('psw'))
    mobilNo = request.form.get('mobno')

    isRegistrationOK = db.registerPlayer(name, email, passwd, mobilNo, competition)

    if isRegistrationOK:
        loginmessage = "Registration completed successfully. Login with your mobile number and password."
        #return render_template("login.html")
        session["competition"] = competition
        session["playername"] = name
        resp = redirect(url_for("login", loginmessage=loginmessage))
        return resp
    else:
        return render_template("registration.html", registrationmessage="Unable to register..")
