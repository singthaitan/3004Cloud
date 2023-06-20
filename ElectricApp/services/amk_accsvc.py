from concurrent import futures
import logging

import grpc
from proto_files import account_pb2
from proto_files import account_pb2_grpc

from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import check_password_hash, generate_password_hash

import re

# Create a new client and connect to the server
client = MongoClient("mongodb+srv://sp:pass@app-cluster.zxcw8od.mongodb.net/", server_api=ServerApi('1'))

# db = client.get_database()
db = client["AngMoKio-Users"]
col_account = db["Account"]
col_household = db["Household"]

class acc_angmokio(account_pb2_grpc.accountServicer):

    def Login(self, request, context):
        email = request.email
        password = request.password

        # Query the database for the user with the given email
        user = col_account.find_one({"e-mail address": email})

        if user:
            # Check if the password matches
            if check_password_hash(user['password'], password):
                # Password matches, perform login
                return account_pb2.Login_Reply(success=True, householdID = str(user["householdID"]))      
            else:
                # Invalid password
                return account_pb2.Login_Reply(success=False)
        else:  
            # Invalid email
            return account_pb2.Login_Reply(success=False)
    

    def Register(self, request, context):
        # Check if the username already exists in the database
        if col_account.find_one({"e-mail address": request.email}):
            return account_pb2.Register_Reply(success=False, error_type="email")
        else:
            # Hash the password
            hashed_password = generate_password_hash(request.password)
            
            # check if address is correct and exist
            # postal_code and unit number must be exactly same
            # street_address can be partial / incomplete and case insensitive
            street_address_pattern = re.sub(r'[^a-zA-Z0-9]+', r'.*', request.address)
            household = col_household.find_one({
                "street_address": {"$regex": f".*{street_address_pattern}.*", "$options": "i"},
                "postal_code": request.postal,
                "unit_number": request.unit
            })

            if not household:
                return account_pb2.Register_Reply(success=False, error_type="address")
            else:
                # Create a new document for the user
                user = {
                    "first name": request.first_name,
                    "last name": request.last_name,
                    "e-mail address": request.email,
                    "password": hashed_password,
                    "region": request.region,
                    "householdID": household["_id"]
                }

                # Insert the document into the collection
                col_account.insert_one(user)
                return account_pb2.Register_Reply(success=True)
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # TODO: Create an instance of your servicer
    account_pb2_grpc.add_accountServicer_to_server(acc_angmokio(),server)
    port = '50051'
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Account service server for Ang Mo Kio started, listening on " + port)
    server.wait_for_termination()

    
if __name__ == '__main__':
    logging.basicConfig()
    serve()
