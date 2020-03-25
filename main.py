from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def connect():
    conn = sqlite3.connect('userinfo.db')
    return conn

def close(conn):
    conn.close()

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/chklogin', methods=['POST', 'GET'])
def chklogin():
    mobilNo = request.args.get('inp_mobile')
    passwd = request.args.get('inp_pass')
    conn = connect()
    cur = conn.cursor()

    sql = "SELECT * FROM USERINFO WHERE mobile='" + str(mobilNo) + "' AND password='" + str(passwd) + "'"
    print(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    
    if len(rows) == 0:
        return render_template("login.html", success="Invalid mobile number/password")
    else:
        sql = "SELECT name FROM USERINFO WHERE mobile='" + str(mobilNo) + "' AND password='" + str(passwd) + "'"
        cur.execute(sql)
        rows = cur.fetchall()
        name = []
        for row in rows:
            name.append(row)

        return render_template("index.html", success="Login successful", welcome = "Welcome " + str(name[0][0]))


@app.route('/senddetails')
def senddetails():
    name = request.args.get('inp_name')
    email = request.args.get('inp_email')
    passwd = request.args.get('inp_pass')
    mobilNo = request.args.get('inp_mobile')

    conn = connect()
    cur = conn.cursor()

    sql = ("INSERT INTO USERINFO VALUES ('" + str(name) + "','" + str(email) + "','" + str(passwd) + "','" + str(mobilNo) + "')")
    cur.execute(sql)
    conn.commit()
    close(conn)

    return render_template("index.html", success="Account created successfully")


@app.route('/signup')
def signup():
    return render_template("registration.html")

@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)