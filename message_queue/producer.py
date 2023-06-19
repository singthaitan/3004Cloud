from kafka import KafkaProducer
import json
import random
import threading
import datetime
import pymongo
from bson import json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

def getAllHouseholdID(household_type, dbRegion):
    # Getting all household id and storing it into a dictionary based on household type
    roomTypeDict = {"1 Room": [],
                "2 Room": [],
                "3 Room": [],
                "4 Room": [],
                "5 Room": [],}
    mydb = myclient[dbRegion]
    collection = mydb["Household"]
    query = {}
    result = collection.find(query)
    for row in result:
        id = row["_id"]
        housing_type = row["housing_type"]
        roomTypeDict[housing_type].append(id)

    listOfID = roomTypeDict[household_type]
    return listOfID

def getRange(timestamp, householdType):
    # rangeDict is for 1 room multiply by 20% for subsequent household types
    rangeDict = {
        "range1": [10,15], # 12am to 6am
        "range2": [25,30], # 7am to 10am
        "range3": [30,40], # 11am to 7pm
        "range4": [35,55] # 8pm to 11pm
    }

    householdTypeMultiplier = 1
    householdTypeNumber = householdType.split()[0]
    for i in range(int(householdTypeNumber)):
        householdTypeMultiplier *= 1.2

    # print(householdTypeMultiplier)

    # timestamp = datetime.datetime(2023, 6, 16, 20, 0, 0, 0)
    hour = timestamp.hour
    rangeType = None
    if 0 <= hour <= 6:
        rangeType = "range1"
    elif 7 <= hour <= 10:
        rangeType = "range2"
    elif 11 <= hour <= 19:
        rangeType = "range3"
    elif 20 <= hour <= 23:
        rangeType = "range4"
    else:
        print("Error in getting range type")

    # print(rangeType)
    return rangeDict[rangeType][0], rangeDict[rangeType][1]

# Household thread
def household_thread(householdType, chosenID, dbRegion, timestamp):
    regionPartition = 0
    if dbRegion == "AngMoKio-Users":
        regionPartition = 0
    elif dbRegion == "Hougang-Users":
        regionPartition = 1
    elif dbRegion == "Jurong-Users":
        regionPartition = 2

    # print("Household1 Count: " + str(householdCount))
    # print("Chosen ID: " + str(chosenID))
    listOfID = getAllHouseholdID(householdType, dbRegion)
    
    # timestamp = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    # timestamp += datetime.timedelta(hours=householdCount)
    # householdCount += 1

    rangeMin, rangeMax = getRange(timestamp, householdType)

    # Reset chosenID
    if chosenID >= len(listOfID):
        chosenID = 0
        timestamp += datetime.timedelta(hours=1)


    # Data to be sent to broker
    producer.send(
        topic_name,
        key={"household_id":parse_json(listOfID[chosenID])},
        value={"timestamp": str(timestamp), "electricity_consumption":float(format(random.uniform(rangeMin, rangeMax), ".2f"))},
        partition=regionPartition
    )
    chosenID += 1

    # Send data every 10 sec (Simulate sending of data every 1 hour)
    threading.Timer(2.0, household_thread, args=[householdType, chosenID, dbRegion, timestamp]).start()

# Setup
hostname = "localhost"
port = "9092"
topic_name = "electricity_consumption"

myclient = pymongo.MongoClient("mongodb+srv://shawn:shawn@app-cluster.zxcw8od.mongodb.net/")
# mydb = myclient["Hougang-Users"]
# collection = mydb["Household"]

# Create producer
producer = KafkaProducer(
    bootstrap_servers = hostname + ":" + str(port),
    value_serializer = lambda v: json.dumps(v).encode('ascii'),
    key_serializer = lambda v: json.dumps(v).encode('ascii')
)

# Start household threads and send them concurrently
chosenID = 0
timestamp = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

# Sending data to hougang region
thread1 = threading.Thread(target=household_thread("1 Room", chosenID, "Hougang-Users", timestamp))
thread1.start()

thread2 = threading.Thread(target=household_thread("2 Room", chosenID, "Hougang-Users", timestamp))
thread2.start()

# Sending data to Ang Mo Kio region
thread3 = threading.Thread(target=household_thread("1 Room", chosenID, "AngMoKio-Users",timestamp))
thread3.start()

thread4 = threading.Thread(target=household_thread("5 Room", chosenID, "AngMoKio-Users",timestamp))
thread4.start()

# Sending data to Jurong region
thread5 = threading.Thread(target=household_thread("1 Room", chosenID, "Jurong-Users",timestamp))
thread5.start()

thread6 = threading.Thread(target=household_thread("5 Room", chosenID, "Jurong-Users",timestamp))
thread6.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()

producer.flush()
