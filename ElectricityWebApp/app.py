from flask import *
from flask_session import Session

import mysql.connector

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return redirect(url_for('login'))
    
@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        if username == 'nicholas' and password == '12345':
            session['username'] = username
            return redirect(url_for('home'))

        else:
            pass

    return render_template('login.html')

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password-repeat']


        if(username != "" and password == password_repeat):
            # mySQL.dbCursor().execute("INSERT INTO accounts (username,password) VALUES (%s,%s)", (username, password))
            # mySQL.dbCommit()
            return redirect(url_for('login'))
        else:
            print("Reach no")
            return render_template('signup.html')

    return render_template('signup.html')
    
@app.route("/home")
def home():
    username = session['username']
    return render_template('index.html',username=username)

@app.route("/getdata",methods=['GET'])
def data():
    if request.method == 'GET':
        # mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="admin",
        #     password="password",
        #     port="3307",
        #     database="hougang_power"
        # )

        # cursor = mydb.cursor()
        # cursor.execute("SELECT * FROM Readings")

        # allResults = cursor.fetchall()

        list = [
            {'address':"block 121 pasir ris street 11",
             'householdType': '3-Room',
             'hour': '2023-06-12 ,14:00',
             'electricity': 1.5},
            {'address':"block 121 pasir ris street 11",
             'householdType': '3-Room',
             'hour': '2023-06-12 ,15:00',
             'electricity': 1.6},
             {'address':"block 121 pasir ris street 11",
             'householdType': '3-Room',
             'hour': '2023-06-12 ,15:00',
             'electricity': 1.7}
        ]

        print(list)
	    
    return jsonify(list)


if __name__ == '__main':
    app.run(debug=True)