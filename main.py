from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def connect():
    conn = sqlite3.connect('userinfo.db')
    return conn

def close(conn):
    conn.close()

@app.route('/senddetails')
def senddetails():
    name = request.args.get('inp_name')
    email = request.args.get('inp_email')
    passwd = request.args.get('inp_pass')

    conn = connect()
    cur = conn.cursor()

    sql = ("INSERT INTO USERINFO VALUES ('" + str(name) + "','" + str(email) + "','" + str(passwd) + "')")
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