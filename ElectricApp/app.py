from flask import *
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import grpc
from proto_files import acc_hougang_pb2
from proto_files import acc_hougang_pb2_grpc
from proto_files import ml_hougang_pb2
from proto_files import ml_hougang_pb2_grpc

# from proto_files import acc_angmokio_pb2
# from proto_files import acc_angmokio_pb2_grpc
# from proto_files import ml_angmokio_pb2
# from proto_files import ml_angmokio_pb2_grpc

# from proto_files import acc_jurong_pb2
# from proto_files import acc_jurong_pb2_grpc
# from proto_files import ml_jurong_pb2
# from proto_files import ml_jurong_pb2_grpc

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


        
        if region == "Hougang":
            session['region'] = "Hougang"
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = acc_hougang_pb2_grpc.acc_HougangStub(channel)
                response = stub.Login(acc_hougang_pb2.Login_Request(email=email, password=password))
                
            if response.success:
                session["householdid"] = response.householdid
                return redirect(url_for('home'))
            else:
                flash('Login failed. Check login credentials.', 'error')
                return render_template('login.html')
        elif region == "AngMoKio":
            session['region'] = "AngMoKio"
            with grpc.insecure_channel('localhost:50053') as channel:
                stub = acc_hougang_pb2_grpc.acc_HougangStub(channel)
                response = stub.Login(acc_hougang_pb2.Login_Request(email=email, password=password))
                
            if response.success:
                session["householdid"] = response.householdid
                return redirect(url_for('home'))
            else:
                flash('Login failed. Check login credentials.', 'error')
                return render_template('login.html')
        elif region == "Jurong":
            session['region'] = "Jurong"

            with grpc.insecure_channel('localhost:50055') as channel:
                stub = acc_hougang_pb2_grpc.acc_HougangStub(channel)
                response = stub.Login(acc_hougang_pb2.Login_Request(email=email, password=password))
                
            if response.success:
                session["householdid"] = response.householdid
                return redirect(url_for('home'))
            else:
                flash('Login failed. Check login credentials.', 'error')
                return render_template('login.html')
        else:
            flash('Invalid region selected.', 'error')
            return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        first_name = request.form['first_name'].lower()
        last_name = request.form['last_name'].lower()
        email = request.form['email'].lower()
        password = request.form['password']
        address = request.form['address'].lower()
        unit = request.form['unit']
        postal = request.form['postal']
        region = request.form['region']
        if region == "Hougang":
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = acc_hougang_pb2_grpc.acc_HougangStub(channel)
                response = stub.Register(acc_hougang_pb2.Register_Request(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    region=region,
                    address=address,
                    unit=unit,
                    postal=postal
                ))

                if response.success == False:
                    if response.error_type == "email":
                        flash('E-mail address already exists. Please login instead.', 'error')
                    elif response.error_type == "address":
                        flash('Address not found, please check Street Address, Unit Number and Postal Code', 'error')
                else:
                    flash('Account registered successfully!', 'success')

        elif region == "AngMoKio":
            with grpc.insecure_channel('localhost:50053') as channel:
                stub = acc_hougang_pb2_grpc.acc_HougangStub(channel)
                response = stub.Register(acc_hougang_pb2.Register_Request(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    region=region,
                    address=address,
                    unit=unit,
                    postal=postal
                ))

                if response.success == False:
                    if response.error_type == "email":
                        flash('E-mail address already exists. Please login instead.', 'error')
                    elif response.error_type == "address":
                        flash('Address not found, please check Street Address, Unit Number and Postal Code', 'error')
                else:
                    flash('Account registered successfully!', 'success')

        elif region == "Jurong":
            with grpc.insecure_channel('localhost:50055') as channel:
                stub = acc_hougang_pb2_grpc.acc_HougangStub(channel)
                response = stub.Register(acc_hougang_pb2.Register_Request(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,region=region,
                    address=address,
                    unit=unit,
                    postal=postal
                ))

                if response.success == False:
                    if response.error_type == "email":
                        flash('E-mail address already exists. Please login instead.', 'error')
                    elif response.error_type == "address":
                        flash('Address not found, please check Street Address, Unit Number and Postal Code', 'error')
                else:
                    flash('Account registered successfully!', 'success')

        # elif region == "AngMoKio":
        #     with grpc.insecure_channel('localhost:50053') as channel:
        #         stub = acc_angmokio_pb2_grpc.acc_AngMoKioStub(channel)
        #         response = stub.Register(acc_angmokio_pb2.Register_Request(
        #             first_name=first_name,
        #             last_name=last_name,
        #             email=email,
        #             password=password,#             region=region,
        #             address=address,
        #             unit=unit,
        #             postal=postal
        #         ))

        #         if response.success == False:
        #             if response.error_type == "email":
        #                 flash('E-mail address already exists. Please login instead.', 'error')
        #             elif response.error_type == "address":
        #                 flash('Address not found, please check Street Address, Unit Number and Postal Code', 'error')
        #         else:
        #             flash('Account registered successfully!', 'success')
        
        # elif region == "Jurong":
        #     with grpc.insecure_channel('localhost:50055') as channel:
        #         stub = acc_jurong_pb2_grpc.acc_JurongStub(channel)
        #         response = stub.Register(acc_jurong_pb2.Register_Request(
        #             first_name=first_name,
        #             last_name=last_name,
        #             email=email,
        #             password=password,region=region,
        #             address=address,
        #             unit=unit,
        #             postal=postal
        #         ))

        #         if response.success == False:
        #             if response.error_type == "email":
        #                 flash('E-mail address already exists. Please login instead.', 'error')
        #             elif response.error_type == "address":
        #                 flash('Address not found, please check Street Address, Unit Number and Postal Code', 'error')
        #         else:
        #             flash('Account registered successfully!', 'success')
                    
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
        
        print(session["viewBy"])

    elif request.method == 'GET':
        session["viewBy"] = 1
        return render_template('index.html')

    return render_template('index.html')


#ML GET DAY DATA / HOUSEID FROM HOUSEHOLD TABLE 
@app.route("/getPastUsage",methods=['GET'])
def data():
    list = []
    if request.method == 'GET':
        if session['region'] == "Hougang":
            with grpc.insecure_channel('localhost:50052') as channel:
                stub = ml_hougang_pb2_grpc.ml_HougangStub(channel)
                response = stub.GetUsageData(ml_hougang_pb2.UsageData_Request(householdid = session["householdid"],
                                                                            days = session["viewBy"]))
                for item in response.items:
                    list.append({'timestamp':item.timestamp, 'electricity':item.electricusage})
        elif session['region'] == "AngMoKio":
            with grpc.insecure_channel('localhost:50054') as channel:
                stub = ml_hougang_pb2_grpc.ml_HougangStub(channel)
                response = stub.GetUsageData(ml_hougang_pb2.UsageData_Request(householdid = session["householdid"],
                                                                            days = session["viewBy"]))
                for item in response.items:
                    list.append({'timestamp':item.timestamp, 'electricity':item.electricusage})

        elif session['region'] == "Jurong":
            with grpc.insecure_channel('localhost:50056') as channel:
                stub = ml_hougang_pb2_grpc.ml_HougangStub(channel)
                response = stub.GetUsageData(ml_hougang_pb2.UsageData_Request(householdid = session["householdid"],
                                                                            days = session["viewBy"]))
                for item in response.items:
                    list.append({'timestamp':item.timestamp, 'electricity':item.electricusage})

        # elif session['region'] == "AngMoKio":
        #     with grpc.insecure_channel('localhost:50054') as channel:
        #         stub = ml_angmokio_pb2_grpc.ml_AngMoKioStub(channel)
        #         response = stub.GetUsageData(ml_angmokio_pb2.UsageData_Request(householdid = session["householdid"],
        #                                                                     days = session["viewBy"]))
        #         for item in response.items:
        #             list.append({'timestamp':item.timestamp, 'electricity':item.electricusage})

        # elif session['region'] == "Jurong":
        #     with grpc.insecure_channel('localhost:50056') as channel:
        #         stub = ml_jurong_pb2_grpc.ml_JurongStub(channel)
        #         response = stub.GetUsageData(ml_jurong_pb2.UsageData_Request(householdid = session["householdid"],
        #                                                                     days = session["viewBy"]))
        #         for item in response.items:
        #             list.append({'timestamp':item.timestamp, 'electricity':item.electricusage})

        #print(list)
        
    return jsonify(list)

#ML GET DAY DATA / HOUSEID FROM HOUSEHOLD TABLE 
@app.route("/getPrediction",methods=['GET'])
def predictedData():
    list = []
    if request.method == 'GET':
        if session['region'] == "Hougang":
            with grpc.insecure_channel('localhost:50052') as channel:
                    stub = ml_hougang_pb2_grpc.ml_HougangStub(channel)
                    response = stub.GetPredictionData(ml_hougang_pb2.PredictionData_Request(householdid = session["householdid"]))# enter householedtype here
                    
                    list1 = []
                    list2 = []
                    for item in response.item:
                        list1.append({'timestamp': item.timestamp, 'electricity': item.electricusage})
                    for item in response.item2:
                        list2.append({'timestamp': item.timestamp, 'electricity': item.electricusage})
        elif session['region'] == "AngMoKio":
            with grpc.insecure_channel('localhost:50054') as channel:
                    stub = ml_hougang_pb2_grpc.ml_HougangStub(channel)
                    response = stub.GetPredictionData(ml_hougang_pb2.PredictionData_Request(householdid = session["householdid"]))# enter householedtype here
                    
                    list1 = []
                    list2 = []
                    for item in response.item:
                        list1.append({'timestamp': item.timestamp, 'electricity': item.electricusage})
                    for item in response.item2:
                        list2.append({'timestamp': item.timestamp, 'electricity': item.electricusage})

        elif session['region'] == "Jurong":
            with grpc.insecure_channel('localhost:50056') as channel:
                    stub = ml_hougang_pb2_grpc.ml_HougangStub(channel)
                    response = stub.GetPredictionData(ml_hougang_pb2_grpc.PredictionData_Request(householdid = session["householdid"]))# enter householedtype here
                    
                    list1 = []
                    list2 = []
                    for item in response.item:
                        list1.append({'timestamp': item.timestamp, 'electricity': item.electricusage})
                    for item in response.item2:
                        list2.append({'timestamp': item.timestamp, 'electricity': item.electricusage})
                    
        # elif session['region'] == "AngMoKio":
        #     with grpc.insecure_channel('localhost:50054') as channel:
        #             stub = ml_angmokio_pb2_grpc.ml_AngMoKioStub(channel)
        #             response = stub.GetPredictionData(ml_angmokio_pb2.PredictionData_Request(householdid = session["householdid"]))# enter householedtype here
                    
        #             list1 = []
        #             list2 = []
        #             for item in response.item:
        #                 list1.append({'timestamp': item.timestamp, 'electricity': item.electricusage})
        #             for item in response.item2:
        #                 list2.append({'timestamp': item.timestamp, 'electricity': item.electricusage})

        # elif session['region'] == "Jurong":
        #     with grpc.insecure_channel('localhost:50056') as channel:
        #             stub = ml_jurong_pb2_grpc.ml_JurongStub(channel)
        #             response = stub.GetPredictionData(ml_jurong_pb2.PredictionData_Request(householdid = session["householdid"]))# enter householedtype here
                    
        #             list1 = []
        #             list2 = []
        #             for item in response.item:
        #                 list1.append({'timestamp': item.timestamp, 'electricity': item.electricusage})
        #             for item in response.item2:
        #                 list2.append({'timestamp': item.timestamp, 'electricity': item.electricusage})
                    
            # print(list1)
            # print(list2)
        
    return jsonify(ownUsage = list1, regionHouseholdUsage = list2)



def viewBY(viewBy):
    return viewBy




if __name__ == '__main':
    app.run(debug=True)