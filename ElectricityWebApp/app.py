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
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the database for the user with the given email
        user = collection.find_one({"e-mail address": email})

        if user:
            # Check if the password matches
            if check_password_hash(user['password'], password):
                # Password matches, perform login
                # ... your login logic ...
                return "Login successful"  # Replace with your desired response

        # Invalid email or password
        return "Invalid email or password"  # Replace with your desired response

    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        unit = request.form['unit']
        postal = request.form['postal']
        household_type = request.form['household_type']
        household_size = request.form['household_size']
        region = request.form['region']

        # Check if the username already exists in the database
        if collection.find_one({"e-mail address": email}):
            return "This e-mail address have already registered for WattWise, please login instead."
        else:
            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create a new document for the user
            user = {
                "first name": first_name,
                "last name": last_name,
                "e-mail address": email,
                "password": hashed_password,
                "street address": address,
                "unit number": unit,
                "postal code": postal,
                "household type": household_type,
                "household size": household_size,
                "region": region
            }

            # Insert the document into the collection
            collection.insert_one(user)

            # Redirect to the login page
            return redirect('/login')
    
@app.route("/home")
def home():
    username = session['username']
    return render_template('index.html',username=username)

# @app.route("/getdata",methods=['GET'])
# def data():
#     if request.method == 'GET':
#         mydb = mysql.connector.connect(
#             host="localhost",
#             user="admin",
#             password="password",
#             port="3307",
#             database="hougang_power"
#         )

#         cursor = mydb.cursor()
#         cursor.execute("SELECT * FROM Readings")

#         allResults = cursor.fetchall()

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
#     return jsonify(readings = allResults)


if __name__ == '__main':
    app.run(debug=True)