from flask import Flask, render_template, request
import grpc
import grpcgateway_pb2
import grpcgateway_pb2_grpc
from concurrent import futures

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve data from the form
    data = request.form['data']

    # Create a PredictRequest message
    predict_request = grpcgateway_pb2.PredictRequest()
    predict_request.data = data

    # Call the Predict RPC method
    predict_response = prediction_stub.Predict(predict_request)

    # Retrieve the prediction from the response
    prediction = predict_response.prediction

    # Create a GetDataRequest message
    get_data_request = grpcgateway_pb2.GetDataRequest()
    get_data_request.id = "123"

    # Call the GetData RPC method
    get_data_response = data_stub.GetData(get_data_request)

    # Retrieve the data from the response
    data = get_data_response.data

    # Create a GetUserRequest message
    get_user_request = grpcgateway_pb2.GetUserRequest()
    get_user_request.id = "456"

    # Call the GetUser RPC method
    get_user_response = account_stub.GetUser(get_user_request)

    # Retrieve the user account information from the response
    user_info = get_user_response.user_info

    # Display the results
    return f"Prediction: {prediction}, Data: {data}, User Info: {user_info}"

def serve_grpc():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # TODO: Add gRPC services to the server if required
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("gRPC server started, listening on " + port)

    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')

    # Create gRPC stubs for all services
    global prediction_stub, data_stub, account_stub
    prediction_stub = grpcgateway_pb2_grpc.PredictionServiceStub(channel)
    data_stub = grpcgateway_pb2_grpc.DataServiceStub(channel)
    account_stub = grpcgateway_pb2_grpc.AccountServiceStub(channel)

    server.wait_for_termination()

if __name__ == '__main__':
    serve_grpc()
    app.run(debug=True)
