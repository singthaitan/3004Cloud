from flask import *
from pymongo import MongoClient
from config import MONGO_URI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)
# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# db = client.get_database()
db = client["ElectricityApp"]
collection = db["users"]

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

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
    return render_template('index.html')

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

	    
#     return jsonify(readings = allResults)


if __name__ == '__main':
    app.run()