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
from bson import ObjectId
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# db = client.get_database()
db = client["Hougang-Electric"]
collection = db["Electricity"]

db_household = client["Hougang-Users"]
collection_household = db_household["Household"]

class ml_Hougang(ml_hougang_pb2_grpc.ml_HougangServicer):

    def GetUsageData(self, request, context):
        houshold_id = ObjectId(request.householdid)
        days = request.days

        # Get current datetime
        timestamp = datetime.now()

        # Subtract 7 days from the timestamp to get the start date
        start_date = timestamp - timedelta(days=days)

        # Convert datetime objects to strings
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print (houshold_id)
        # Query the collection for documents where the timestamp is between start_date_str and timestamp_str
        # Replace "your_timestamp_field" with the field in your collection that holds the timestamp
        results = collection.find({
            "timestamp": {"$gte": start_date_str, "$lt": timestamp_str},
            "household_id": houshold_id
        })


        reply = ml_hougang_pb2.UsageData_Reply()
        for doc in results:
            print( doc['timestamp'])
            item = ml_hougang_pb2.UsageData()
            item.timestamp = doc['timestamp']
            item.electricusage = doc['electricity_consumption']
            reply.items.append(item)

        return reply
    
    def GetPredictionData(self, request, context):
        print("aaaaaaaaaaa" +request.householdid)
        household_id = ObjectId(request.householdid)

        #for housing type
        # household = collection_household.find_one({"_id" : household_id})
        # print("bbbbbbb" +household["housing_type"])

        # Query past 30 days data of the given household
        pipeline = [
            {"$match": {"household_id": household_id}},
            {"$sort": {"timestamp": -1}},  # sort by timestamp in descending order
            {"$limit": 24*30}  # get the past 30 days data
        ]
        data = list(collection.aggregate(pipeline))

        # Convert the data to pandas DataFrame
        df = pd.DataFrame(data)

        # Convert the 'timestamp' column to datetime type
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Set 'timestamp' as the index of the dataframe
        df.set_index('timestamp', inplace=True)

        # Calculate moving average over a 30-day period for each hour
        hourly_avg = df.groupby(df.index.hour).mean()
        hourly_avg = hourly_avg.reindex(range(0, 24), fill_value=0)

        reply = ml_hougang_pb2.PredictionData_Reply()
        current_hour = datetime.now().hour

        # Add prediction items for the next 24 hours based on the hourly average
        for i in range(24):
            next_hour = (current_hour + i) % 24
            next_timestamp = (datetime.now() + timedelta(hours=i)).strftime("%Y-%m-%d %H:00:00")

            # prediction item for individual
            item = reply.item.add()
            item.timestamp = next_timestamp
            item.electricusage = float(hourly_avg.loc[next_hour, 'electricity_consumption'])

        
        return reply



        reply = ml_hougang_pb2.PredictionData_Reply()

        # prediction item for individual
        item1 = reply.item.add()
        item1.timestamp = "2023-06-16 12:00:00"
        item1.electricusage = 5.0

        item2 = reply.item.add()
        item2.timestamp = "2023-06-16 13:00:00"
        item2.electricusage = 6.0

        # prediction item for housing type
        item3 = reply.item2.add()
        item3.timestamp = "2023-06-16 12:00:00"
        item3.electricusage = 10.0

        item4 = reply.item2.add()
        item4.timestamp = "2023-06-16 13:00:00"
        item4.electricusage = 12.0

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
        



