from flask import *
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import grpc
from proto_files import account_pb2
from proto_files import account_pb2_grpc
from proto_files import ml_pb2
from proto_files import ml_pb2_grpc

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
        email = request.form['email'].lower()
        password = request.form['password']
        region = request.form["region"]
        session['region'] = region

        grpc_port = {
            "AngMoKio": "50051",
            "Hougang": "50053",
            "Jurong": "50055"
        }
        channel_port = grpc_port.get(region)

        if channel_port:
            with grpc.insecure_channel(f'localhost:{channel_port}') as channel:
                stub = account_pb2_grpc.accountStub(channel)
                response = stub.Login(account_pb2.Login_Request(email=email, password=password))

                if response.success is False:
                    flash('Login failed. Check login credentials.', 'error')
                else:
                    session["householdID"] = response.householdID
                    return redirect(url_for('home'))

        return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        region = request.form['region']
        grpc_port = {
            "AngMoKio": "50051",
            "Hougang": "50053",
            "Jurong": "50055"
        }
        channel_port = grpc_port.get(region)

        if channel_port:
            with grpc.insecure_channel(f'localhost:{channel_port}') as channel:
                stub = account_pb2_grpc.accountStub(channel)
                response = stub.Register(account_pb2.Register_Request(
                    first_name=request.form['first_name'].lower(),
                    last_name=request.form['last_name'].lower(),
                    email=request.form['email'].lower(),
                    password=request.form['password'],
                    region=region,
                    address=request.form['address'].lower(),
                    unit=request.form['unit'],
                    postal=request.form['postal']
                ))

                if response.success is False:
                    if response.error_type == "email":
                        flash('E-mail address already exists. Please login instead.', 'error')
                    elif response.error_type == "address":
                        flash('Address not found, please check Street Address, Unit Number and Postal Code', 'error')
                else:
                    flash('Account registered successfully!', 'success')

        return render_template('register.html')


@app.route("/home", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        view = request.form["viewBy"]
        if view == "monthly":
            session["viewBy"] = 30
        elif view == "weekly": 
            session["viewBy"] = 7
        elif view == "daily": 
            session["viewBy"] = 1

    elif request.method == 'GET':
        session["viewBy"] = 1
        return render_template('index.html')

    return render_template('index.html')


#ML GET DAY DATA / HOUSEID FROM HOUSEHOLD TABLE 
@app.route("/getPastUsage", methods=['GET'])
def data():
    usage_list = []
    
    if session['region'] == "AngMoKio":
        channel_port = '50052'
    elif session['region'] == "Hougang":
        channel_port = '50054'
    elif session['region'] == "Jurong":
        channel_port = '50056'

    with grpc.insecure_channel(f'localhost:{channel_port}') as channel:
        stub = ml_pb2_grpc.mlStub(channel)
        response = stub.GetUsageData(ml_pb2.UsageData_Request(
            householdID=session["householdID"],
            days=session["viewBy"]))

        for item in response.items:
            usage_list.append({'timestamp': item.timestamp, 'electricity': item.electric_usage})

    return jsonify(usage_list)


#ML GET DAY DATA / HOUSEID FROM HOUSEHOLD TABLE 
@app.route("/getPrediction", methods=['GET'])
def predictedData():
    list1 = [] 
    list2 = []
    
    if session['region'] == "AngMoKio":
        channel_port = '50052'
    elif session['region'] == "Hougang":
        channel_port = '50054'
    elif session['region'] == "Jurong":
        channel_port = '50056'
    
    with grpc.insecure_channel(f'localhost:{channel_port}') as channel:
        stub = ml_pb2_grpc.mlStub(channel)
        response = stub.GetPredictionData(ml_pb2.PredictionData_Request(householdID=session["householdID"]))
        
        for item in response.item:
            list1.append({'timestamp': item.timestamp, 'electricity': item.electric_usage})
        
        for item in response.item2:
            list2.append({'timestamp': item.timestamp, 'electricity': item.electric_usage})
    
    return jsonify(ownUsage=list1, regionHouseholdUsage=list2)


def viewBY(viewBy):
    return viewBy


if __name__ == '__main__':
    app.run(debug=True)