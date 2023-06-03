from flask import *
import mysql.connector

app = Flask(__name__)

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
        if(password == password_repeat):
            print("Reach")
            # mySQL.dbCursor().execute("INSERT INTO accounts (username,password) VALUES (%s,%s)", (username, password))
            # mySQL.dbCommit()
            return redirect(url_for('login'))
        else:
            print("Reach no")
            return render_template('signup.html')

    return render_template('signup.html')
    
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/getdata",methods=['GET'])
def data():
    if request.method == 'GET':
        mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="password",
            port="3307",
            database="hougang_power"
        )

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM Readings")

        allResults = cursor.fetchall()

	    
    return jsonify(readings = allResults)


if __name__ == '__main':
    app.run()