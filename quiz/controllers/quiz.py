from flask import render_template, request, session
import datetime
from repositories import db
import flask

def question():
    #player_id = request.cookies.get("playerid")
    player_id = session["mobileno"]
    competition_name = session["competition"]
    player_name = session["playername"]

    #print (player_id, competition_name)

    #rowDict = {"competition": competition_name}

    current_quiz_qna = db.getQuizQuestion(player_id, competition_name)

    if len(current_quiz_qna) == 0:
        quizmessage = "No active question. Please try again later."
    else:
        quizmessage = "Current active question."

    return render_template("quiz.html", playername=player_name, questionmessage=quizmessage, dbqna=current_quiz_qna)

def answer():
    player_id = session["mobileno"]
    competition_name =session["competition"]

    qid = request.form.get("qid")
    qdesc = request.form.get("qdesc")
    points = request.form.get("points")
    ans = request.form.get("choice")
    negativepoints = request.form.get("negativepoints")

    resptime = datetime.datetime.now()

    questionmessage = ""

    isResponded = db.isResponded(player_id, qid)

    if isResponded == True:
        questionmessage = "You have already responded."
    else:
        correct_ans = db.getAnswer(competition_name, qid)

        if correct_ans != ans:
            points = negativepoints

        isRegisterOK = db.registerResponse(player_id, competition_name, qid, qdesc, ans, resptime, points)

        if isRegisterOK:
            questionmessage = "Your response registered successfully"
        else:
            questionmessage = "Unable to register response."

    current_quiz_qna = db.getQuizQuestion(player_id, competition_name)

    if not bool(current_quiz_qna.items):
        questionmessage = "No more active question at this time.."

    return render_template("quiz.html", questionmessage=questionmessage, dbqna=current_quiz_qna)
