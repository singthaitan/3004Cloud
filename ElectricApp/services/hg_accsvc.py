from concurrent import futures
import logging

from proto_files import acc_hougang_pb2
from proto_files import acc_hougang_pb2_grpc
import grpc
from pymongo import MongoClient
from services.hg_config import MONGO_URI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import check_password_hash, generate_password_hash

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# db = client.get_database()
db = client["ElectricityApp"]
collection = db["users"]

class acc_Hougang(acc_hougang_pb2_grpc.acc_HougangServicer):

    def Login(self,request,context):
        print("b")
        email = request.email
        password = request.password

        # Query the database for the user with the given email
        user = collection.find_one({"e-mail address": email})

        if user:
            # Check if the password matches
            if check_password_hash(user['password'], password):
                # Password matches, perform login
                # ... your login logic ...
                return acc_hougang_pb2.Login_Reply(success=True)  # Replace with your desired response

        # Invalid email or password
        return acc_hougang_pb2.Login_Reply(success=False)  # Replace with your desired response
    

    def Register(self, request, context):
        print("a")
        # Check if the username already exists in the database
        if collection.find_one({"e-mail address": request.email}):

            return acc_hougang_pb2.Register_Reply(success=False)
        else:
            # Hash the password
            hashed_password = generate_password_hash(request.password)

            # Create a new document for the user
            user = {
                "first name": request.first_name,
                "last name": request.last_name,
                "e-mail address": request.email,
                "password": hashed_password,
                # "street address": address,
                # "unit number": unit,
                # "postal code": postal,
                # "household type": household_type,
                # "household size": household_size,
                "region": request.region

                #add householdid check if it exists too
            }

            # Insert the document into the collection
            collection.insert_one(user)
        return acc_hougang_pb2.Register_Reply(success=True)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # TODO: Create an instance of your servicer
    acc_hougang_pb2_grpc.add_acc_HougangServicer_to_server(acc_Hougang(),server)
    pass

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


    
if __name__ == '__main__':
    logging.basicConfig()
    serve()



# message Login_Request {
#     string email =1;
#     string password = 2;
# }

# message Login_Reply {
#     bool success = 1;
# }