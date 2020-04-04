from flask import render_template, request, make_response, redirect, url_for, session
from repositories import db
import flask
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

#@app.route('/login')
def login():
    loginmessage = request.args.get('loginmessage')

    if loginmessage is None:
        loginmessage = ""
    
    return render_template("login.html", loginmessage=loginmessage)

#@app.route('/adminlogin')
def adminlogin():
    email = request.args.get('inp_email')
    passwd = request.args.get('inp_pass')
    if email == "pkh_p@hotmail.com" and passwd == "pkh1234":
        return render_template("addQuestion.html")
    else:
        return render_template("admin.html", success="Invalid email/password")

#@app.route('/loginsubmit', methods=['POST', 'GET'])
def chklogin():
    mobileNo = request.form.get('uname')
    passwd = request.form.get('psw')
    remember = request.form.get('remember')

    playenrname, competition, playerpwd = db.CheckLogin(mobileNo)
    if len(playenrname) > 0:
        if check_password_hash(playerpwd, passwd):    
            session["mobileno"] = mobileNo
            session["competition"] = competition
            session["playername"] = playenrname

            questionmessage = "You are logged in"
            resp = make_response(redirect(url_for("question", questionmessage=questionmessage)))
            
            if (remember == "on"):
                resp.set_cookie("playerid", mobileNo, max_age=1)
            
            return resp
        else:
            return render_template("login.html", loginmessage="Invalid mobile number/password")
    else:
        return render_template("login.html", loginmessage="Invalid mobile number/password")
    