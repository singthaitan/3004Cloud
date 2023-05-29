from flask import *
import mysql.connector

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

# @app.route("/getdata",methods=['GET'])
# def data():
#     if flask.request.method == 'GET':
       
#             date = datetime.now()
#             date_str = date.strftime("%d/%m/%Y %H:%M:%S")
#             sensor = message[0]
#             sensor_data = float(message[1])

#             print(sensor +":"+ str(sensor_data))
                      
	    
#     return jsonify(sensor = sensor, sensor_data = sensor_data,date = date_str, date1 = date_str)


if __name__ == '__main':
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        port="3307",
        database="hougang_power"
    )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
    app.run()