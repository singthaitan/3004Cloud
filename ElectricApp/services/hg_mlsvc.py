from concurrent import futures
import logging

from proto_files import ml_hougang_pb2
from proto_files import ml_hougang_pb2_grpc
import grpc
from pymongo import MongoClient
from services.hg_config import MONGO_URI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta


# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# db = client.get_database()
db = client["HougangElectric"]
collection = db["Electricity"]

class ml_Hougang(ml_hougang_pb2_grpc.ml_HougangServicer):

    def GetUsageData(self, request, context):
        houshold_id = request.householdid
        days = request.days

        # Get current datetime
        timestamp = datetime.now()

        # Subtract 7 days from the timestamp to get the start date
        start_date = timestamp - timedelta(days=days)

        # Convert datetime objects to strings
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Query the collection for documents where the timestamp is between start_date_str and timestamp_str
        # Replace "your_timestamp_field" with the field in your collection that holds the timestamp
        results = collection.find({
            "timestamp": {"$gte": start_date_str, "$lt": timestamp_str},
            "householdid": houshold_id
        })

        reply = ml_hougang_pb2.UsageData_Reply()
        for doc in results:
            item = ml_hougang_pb2.UsageData()
            item.timestamp = doc['timestamp']
            item.electricusage = doc['electric_usage']
            reply.items.append(item)

        return reply


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ml_hougang_pb2_grpc.add_ml_HougangServicer_to_server(ml_Hougang(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
        



