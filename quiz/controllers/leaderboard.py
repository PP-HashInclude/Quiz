from flask import render_template, session
from repositories import db

def leaderboard():
    playerid = ""
    statusmessage = ""
    dbrows = []

    try:
        playerid = session.get("mobileno")
        
        if playerid is None:
            statusmessage = "Please login to view your score"
        else:
            dbrows = db.getScore(playerid)
    except Exception as ex:
        print ("Error: ", ex)
        statusmessage = "Unable to load data."
    
    return render_template("leaderboard.html", reportMessage=statusmessage, dbrows=dbrows)

def ranks():
    dbrows = db.getRanks()
    return render_template("rankreport.html", dbrows=dbrows)