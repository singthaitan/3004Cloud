# import flask
# from flask import request, redirect, render_template, url_for
from flask import *
from pymongo import MongoClient
# from config import MONGO_URI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import check_password_hash, generate_password_hash
from proto_files import acc_hougang_pb2
from proto_files import acc_hougang_pb2_grpc
import grpc


app = Flask(__name__)

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
                return "Login successful"
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
        address = request.form['address']
        unit = request.form['unit']
        postal = request.form['postal']
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
                                                                          region = region, 
                                                                          address = address,
                                                                          unit = unit,
                                                                          postal = postal))
                print(response.success)
                


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
    create_app().run()