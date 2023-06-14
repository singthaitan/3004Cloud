from flask import *
from pymongo import MongoClient
# from config import MONGO_URI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import check_password_hash, generate_password_hash
from proto_files import acc_hougang_pb2
from proto_files import acc_hougang_pb2_grpc
from proto_files import ml_hougang_pb2
from proto_files import ml_hougang_pb2_grpc
import grpc
from flask_session import Session



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
        region = request.form["region"]
        if region == "hougang":
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = acc_hougang_pb2_grpc.acc_HougangStub(channel)

                response = stub.Login(acc_hougang_pb2.Login_Request(email = email, password = password))
                
            if response.success == True:
                session["householdid"] = response.householdid
                return redirect(url_for('home'))
            else:
                return "Invalid email or password"


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
        # address = request.form['address']
        # unit = request.form['unit']
        # postal = request.form['postal']
        # household_type = request.form['household_type']
        # household_size = request.form['household_size']
        region = request.form['region']
        print(region)

        if region == "Hougang":
            with grpc.insecure_channel('localhost:50051') as channel:
                print("aaaaa")
                stub = acc_hougang_pb2_grpc.acc_HougangStub(channel)
                response = stub.Register(acc_hougang_pb2.Register_Request(first_name = first_name,
                                                                          last_name = last_name,
                                                                          email = email, 
                                                                          password = password,
                                                                          region = region))
                print(response.success)
                


            # Redirect to the login page
            return redirect('/login')
    
@app.route("/home")
def home():
    return render_template('index.html')



#ML GET  DAY DATA /GET HOUSEID FROM HOUSEHOLD TABLE 
@app.route("/getdata",methods=['GET'])
def data():
    if request.method == 'GET':
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = ml_hougang_pb2_grpc.ml_HougangStub(channel)
            response = stub.GetUsageData(ml_hougang_pb2.UsageData_Request(householdid = session["householdid"],
                                                                          days = 7))
            for item in response.items:
                print(f"Timestamp: {item.timestamp}, Electricity usage: {item.electricusage}")

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
