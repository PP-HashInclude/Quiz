
from common import config
import sqlite3

dbfile = config.getdbfile()

def opendb():
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    return conn, c

def quote_fix(string):
    new_string = ""
    for i in range(len(string)):
        if string[i] == "'":
            new_string += "'"
        new_string += string[i]
    return new_string

def getQuizQuestion(playerid, competition_name):
    con, cur = opendb()
    
    strSql = "SELECT QId, Quesdesc, Choice1,Choice2,Choice3,Choice4,ValidTill,Points,NegativePoints FROM QuestionBank WHERE CompetitionName = 'Lockdown-2020 Quiz' AND datetime(ValidTill) > datetime('now') AND QId not in (select QId from PlayerResponse WHERE PlayerResponse.QId = QuestionBank.QId AND PlayerResponse.PlayerId = '" + playerid + "') ORDER BY datetime(ValidTill) ASC LIMIT 1"
    
    #print (strSql)

    cur.execute(strSql)

    rows = cur.fetchall()
    
    cur.close()
    con.close()

    qid = ""
    qdesc = ""
    ch1 = ""
    ch2 = ""
    ch3 = ""
    ch4 = ""
    validtill = ""
    points = ""
    negativepoints = ""

    rowDict = {}
    
    for item in rows:
        qid = item[0]
        qdesc = item[1]
        ch1 = item[2]
        ch2 = item[3]
        ch3 = item[4]
        ch4 = item[5]
        validtill = item[6]
        points = item[7]
        negativepoints = item[8]
    
        rowDict = {"qid": qid,
                    "qdesc": qdesc,
                    "ch1": ch1,
                    "ch2": ch2,
                    "ch3": ch3,
                    "ch4": ch4,
                    "validtill": validtill,
                    "points": points,
                    "negativepoints": negativepoints
                    }
    
    return rowDict

def createQuestion(qno, ques_desc, choice1, choice2, choice3, choice4, choice_right, valid_till):
    conn, cur = opendb()
    
    sql = "INSERT INTO QuestionBank VALUES (" + str(qno) + ",'" + quote_fix(str(choice1)) + "','" + quote_fix(str(choice2)) + "','" + quote_fix(str(choice3)) + "','" + quote_fix(str(choice4)) + "','" + quote_fix(str(choice_right)) + "','" + quote_fix(str(ques_desc)) + "', datetime('" + str(valid_till) + "'))"
    #print(sql)

    cur.execute(str(sql))
    
    conn.commit()

    cur.close()
    conn.close()

def CheckLogin(loginid):
    sql = "SELECT name, competitionname, password FROM Players WHERE mobile = " + str(loginid)
    
    conn, cur = opendb()

    cur.execute(sql)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    if len(rows) > 0:
        playername = rows[0][0]
        competition = rows[0][1]
        playerpwd = rows[0][2]
    else:
        playername = ""
        competition = ""
        playerpwd = ""
    
    return playername, competition, playerpwd

def registerPlayer(name, email, passwd, mobileNo, competitionname):
    isRegistrationOK = False
    try:
        conn, cur = opendb()
    
        sql = "INSERT INTO Players VALUES ('" + str(name) + "','" + str(email) + "','" + str(passwd) + "', " + mobileNo + ", '" + str(competitionname) + "')"
        #print(sql)

        cur.execute(str(sql))

        conn.commit()

        cur.close()
        conn.close()

        isRegistrationOK = True
    except Exception as ex:
        print(ex)
        #pass
    
    return isRegistrationOK

def getCompetitions():
    sql = "SELECT name FROM competition WHERE datetime('now') < datetime(EndingOn)"
    
    conn, cur = opendb()

    cur.execute(sql)
    dbrows = cur.fetchall()

    cur.close()
    conn.close()

    return dbrows

def isResponded(player_id, qid):
    conn, cur = opendb()
    
    sql = "SELECT * FROM PlayerResponse WHERE PlayerId = " + player_id + " AND QId = " + qid

    cur.execute(sql)
    rows = cur.fetchall()
    
    conn.commit()

    cur.close()
    conn.close()

    isResponded = False

    if len(rows) > 0:
        isResponded = True
    
    return isResponded

def registerResponse(player_id, competition_name, qid, qdesc, ans, resptime, points):
    isRegisterOK = True
    try:
        conn, cur = opendb()
        
        sql = "INSERT INTO PlayerResponse VALUES("
        sql += player_id + ", "
        sql += "'" + competition_name + "', "
        sql += qid + ", "
        sql += "'" + qdesc + "', "
        sql += "'" + ans + "', "
        sql += "'" + str(resptime) + "', "
        sql += points + ")"

        cur.execute(sql)
        rows = cur.fetchall()
        
        conn.commit()

        cur.close()
        conn.close()
    except Exception as ex:
            isRegisterOK = False
    
    return isRegisterOK

def getScore(playerid):
    conn,  cur = opendb()
    sql = "SELECT name, pr.CompetitionName, pr.Question, Points FROM PlayerResponse pr, Players p WHERE p.mobile = " + playerid + " AND pr.PlayerId = p.mobile ORDER BY Points DESC"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def getRanks():
    conn,  cur = opendb()
    sql = "SELECT name, pr.competitionname as competionname, sum(points) as totalpoints, \
        RANK () OVER ( \
        ORDER BY sum(points) DESC \
        ) pointrank \
        FROM PlayerResponse pr, Players p \
        WHERE pr.PlayerId = p.mobile \
        GROUP BY name, pr.competitionname \
        ORDER BY sum(Points) DESC"

    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def getAccount(playerid):
    conn,  cur = opendb()
    sql = "SELECT name, email, mobile, competitionname FROM Players WHERE mobile = " + str(playerid)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    rowDict = {}

    if len(rows) > 0:
        rowDict = {"playername": rows[0][0],
            "email": rows[0][1],
            "playerid": rows[0][2],
            "competitionname": rows[0][3]
            }
    
    return rowDict

def updateProfile(mobilNo, playername, email, competition):
    isUpdateOK = True

    try:
        sql = "UPDATE Players SET \
                name = '" + playername + "', \
                email = '" + email + "', \
                competitionname = '" + competition + "' \
            WHERE mobile = " + str(mobilNo)
        conn,  cur = opendb()
        cur.execute(sql)
        rows = cur.fetchall()
        
        conn.commit()

        cur.close()
        conn.close()
    except Exception as ex:
        isUpdateOK = False

    return isUpdateOK


def UpdatePassword(mobileNo, npasswd1):
    isUpdateOK = True

    try:
        sql = "UPDATE Players SET \
                password = '" + npasswd1 + "' \
            WHERE mobile = " + str(mobileNo)

        conn,  cur = opendb()
        cur.execute(sql)
        rows = cur.fetchall()
        
        conn.commit()

        cur.close()
        conn.close()
    except Exception as ex:
        print (ex)
        isUpdateOK = False

    return isUpdateOK

def getAnswer(competition_name, qid):
    conn,  cur = opendb()
    sql = "SELECT ChoiceAnswer FROM QuestionBank WHERE Qid = " + str(qid) + " AND CompetitionName = '" + competition_name + "'"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    rowDict = {}
    answer = ""

    if len(rows) > 0:
        answer = rows[0][0]
    
    return answer
