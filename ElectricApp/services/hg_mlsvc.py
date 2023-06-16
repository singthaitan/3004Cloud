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
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
import os


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
        household = collection_household.find_one({"_id" : household_id})
        print("bbbbbbb" +household["housing_type"])
        householdprediction = getElectricityPredictions(household["housing_type"])

        print(householdprediction)

        # The current time, rounded to the next hour
        current_time = datetime.now()
        minutes_past = current_time.minute if current_time.minute != 0 else 60
        current_time += timedelta(minutes=minutes_past)

        reply = ml_hougang_pb2.PredictionData_Reply()

        for i in range(24):  # for the next 24 hours
            item = reply.item2.add()
            item.timestamp = (current_time + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S")
            item.electricusage = householdprediction[i]
        


        # # Query past 30 days data of the given household
        # pipeline = [
        #     {"$match": {"household_id": household_id}},
        #     {"$sort": {"timestamp": -1}},  # sort by timestamp in descending order
        #     {"$limit": 24*30}  # get the past 30 days data
        # ]
        # data = list(collection.aggregate(pipeline))

        # # Convert the data to pandas DataFrame
        # df = pd.DataFrame(data)

        # # Convert the 'timestamp' column to datetime type
        # df['timestamp'] = pd.to_datetime(df['timestamp'])

        # # Set 'timestamp' as the index of the dataframe
        # df.set_index('timestamp', inplace=True)

        # # Calculate moving average over a 30-day period for each hour
        # hourly_avg = df.groupby(df.index.hour).mean()
        # hourly_avg = hourly_avg.reindex(range(0, 24), fill_value=0)

        # reply = ml_hougang_pb2.PredictionData_Reply()
        # current_hour = datetime.now().hour

        # # Add prediction items for the next 24 hours based on the hourly average
        # for i in range(24):
        #     next_hour = (current_hour + i) % 24
        #     next_timestamp = (datetime.now() + timedelta(hours=i)).strftime("%Y-%m-%d %H:00:00")

        #     # prediction item for individual
        #     item = reply.item.add()
        #     item.timestamp = next_timestamp
        #     item.electricusage = float(hourly_avg.loc[next_hour, 'electricity_consumption'])

        # return reply

        # prediction item for individual
        item1 = reply.item.add()
        item1.timestamp = "2023-06-16 12:00:00"
        item1.electricusage = 5.0

        item2 = reply.item.add()
        item2.timestamp = "2023-06-16 13:00:00"
        item2.electricusage = 6.0

        # # prediction item for housing type
        # item3 = reply.item2.add()
        # item3.timestamp = "2023-06-16 12:00:00"
        # item3.electricusage = 10.0

        # item4 = reply.item2.add()
        # item4.timestamp = "2023-06-16 13:00:00"
        # item4.electricusage = 12.0

        return reply




def getElectricityPredictions(household_type):
    def getAllHouseholdID(household_type):
        # Create an empty dictionary that stores each room type household ids
        roomTypeDict = {"1 Room": [], "2 Room": [], "3 Room": [], "4 Room": [], "5 Room": []}

        # Query from Household collection

        query = {}
        result = collection_household.find(query)
        for row in result:
            id = row["_id"]
            housing_type = row["housing_type"]
            roomTypeDict[housing_type].append(id)

        listOfID = roomTypeDict[household_type]
        return listOfID



    # Get household ID based on household type
    listOfHouseholdID = getAllHouseholdID(household_type)
    dataset = []
    predictions = []

    # Get all records from listOfHouseholdID in Electricity collection
    query = {"household_id": {"$in": listOfHouseholdID}}
    result = collection.find(query)
    df = pd.DataFrame(list(result))
    dataset = df.tail(73)
    dataset['electricity_consumption'] = pd.to_numeric(dataset['electricity_consumption'], errors='coerce')
    dataset = dataset['electricity_consumption'].tolist()

    # Load the model based on household_type
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(os.path.dirname(current_dir), "models")
    model_name = os.path.join(models_dir, f"{household_type.lower().replace(' ', '_')}_model.h5")
    model = keras.models.load_model(model_name)

    model = keras.models.load_model(model_name)

    # Reshape the numpy array into a 2D array with 1 column
    dataset = np.reshape(dataset, (-1, 1))

    # Create an instance of the MinMaxScaler class to scale the values between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))

    # Fit the MinMaxScaler to the transformed data and transform the values
    dataset = scaler.fit_transform(dataset)

    # convert an array of values into a dataset matrix
    def create_dataset(dataset, look_back=48):
        X = []
        for i in range(len(dataset) - look_back - 1):
            a = dataset[i:(i + look_back), 0]
            X.append(a)
        return np.array(X)

    # reshape into X=t and Y=t+1
    look_back = 48
    X_test = create_dataset(dataset, look_back)

    # reshape input to be [samples, time steps, features]
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # make predictions
    test_predict = model.predict(X_test)

    # invert predictions
    test_predict = scaler.inverse_transform(test_predict)

    for i in range(24):
        prediction = test_predict[i, 0]
        predictions.append(prediction)

    return predictions


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ml_hougang_pb2_grpc.add_ml_HougangServicer_to_server(ml_Hougang(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
        



