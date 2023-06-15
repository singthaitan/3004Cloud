from kafka import KafkaProducer
import json
import random
import threading
import datetime
import pymongo
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

def getAllHouseholdID(household_type):
    # Getting all household id and storing it into a dictionary based on household type
    roomTypeDict = {"1 Room": [],
                "2 Room": [],
                "3 Room": [],
                "4 Room": [],
                "5 Room": [],}
    mydb = myclient["Hougang-Users"]
    collection = mydb["Household"]
    query = {}
    result = collection.find(query)
    for row in result:
        id = row["_id"]
        housing_type = row["housing_type"]
        roomTypeDict[housing_type].append(id)

    listOfID = roomTypeDict[household_type]
    return listOfID

# Household 1
household1Count = 0
def household1_thread():
    global household1Count
    listOfID = getAllHouseholdID("1 Room")
    # Send data every 10 sec (Simulate sending of data every 1 hour)
    threading.Timer(10.0, household1_thread).start()
    timestamp = datetime.datetime.now().replace(minute=0, microsecond=0)
    household1Count += 1

    # Data to be sent to broker
    producer.send(
        topic_name,
        key={"household_id":parse_json(listOfID[household1Count % 2])},
        value={"timestamp": str(timestamp), "electricity_consumption":float(format(random.uniform(1.776, 393.632), ".2f"))}
    )

# Household 2
household2Count = 0
def household2_thread():
    global household2Count
    listOfID = getAllHouseholdID("2 Room")
    # Send data every 10 sec (Simulate sending of data every 1 hour)
    threading.Timer(10.0, household2_thread).start()
    timestamp = datetime.datetime.now().replace(minute=0, microsecond=0)
    household2Count += 1

    # Data to be sent to broker
    producer.send(
        topic_name,
        key={"household_id":parse_json(listOfID[household2Count % 2])},
        value={"timestamp": str(timestamp), "electricity_consumption":float(format(random.uniform(2.1312, 472.3584), ".2f"))}
    )

# Setup
hostname = "localhost"
port = "9092"
topic_name = "test"

myclient = pymongo.MongoClient("mongodb+srv://shawn:shawn@app-cluster.zxcw8od.mongodb.net/")
mydb = myclient["Hougang-Users"]
collection = mydb["Household"]

# Create producer
producer = KafkaProducer(
    bootstrap_servers = hostname + ":" + str(port),
    value_serializer = lambda v: json.dumps(v).encode('ascii'),
    key_serializer = lambda v: json.dumps(v).encode('ascii')
)

# Start both household threads and send them concurrently
thread1 = threading.Thread(target=household1_thread)
thread1.start()

thread2 = threading.Thread(target=household2_thread)
thread2.start()

thread1.join()
thread2.join()

producer.flush()
