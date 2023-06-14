# Import necessary libraries and packages
import numpy as np

#import matplotlib.pyplot as plt
import pandas as pd

# Set floating point precision option for pandas
pd.set_option('display.float_format', lambda x: '%.4f' % x)

# Import seaborn library and set context and style
import seaborn as sns
sns.set_context("paper", font_scale=1.3)
sns.set_style('white')

# Import warnings and set filter to ignore warnings
import warnings
warnings.filterwarnings('ignore')


# Import MongoDB
import pymongo
# import pandas as pd
import datetime

# Set up Mongodb Atlas
myclient = pymongo.MongoClient("mongodb+srv://shawn:shawn@app-cluster.zxcw8od.mongodb.net/")
mydb = myclient["Hougang-Users"]
collection = mydb["Household"]


# Get household ID based on household type
listOfHouseholdID = []
household_type = "5 Room"
query = {"housing_type": household_type}
cursor = collection.find(query)
for document in cursor:
    household_id = document["_id"]
    listOfHouseholdID.append(household_id)

# Get all records from listOfHouseholdID in electricity_consumption collection
mydb = myclient["Hougang-Electric"]
collection = mydb["Electricity"]
query = {"household_id": {"$in": listOfHouseholdID}}
result = collection.find(query)

for row in result:
    timestamp = row["timestamp"]
    electricity_consumption = row["electricity_consumption"]
    # print("The timestamp is: " + timestamp + "\n" + "The electricity consumption is: " + str(electricity_consumption) + "\n")
    print(row)

# Uncomment code below if uploading data into mongodb
# Getting all household id and storing it into a dictionary based on household type
"""
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

# Inserting records from all 5 csvs into database
mydb = myclient["Hougang-Electric"]
collection = mydb["Electricity"]

numberOfRecordsAdded = 0
for roomNo in range(1, 6):
    household_type = str(roomNo) + " Room"
    listOfID = roomTypeDict[household_type]
    # for i in listOfID:
    #     print(i)
    data = pd.read_csv("hourly_" + str(roomNo) +"_room_dataset.csv", nrows=24)

    listOfElecCons = []
    data.columns = ["electricity_consumption"]
    for i in data["electricity_consumption"]:
        listOfElecCons.append(i)

    timestamp = datetime.datetime(2010, 1, 1)
    for i in range(len(listOfElecCons)):
        if i != 0:
            timestamp = timestamp + datetime.timedelta(hours=1)
        mongoData = {"timestamp": str(timestamp),
                    "electricity_consumption": listOfElecCons[i],
                    "household_id": listOfID[i % 2]}
        insert_result = collection.insert_one(mongoData)
        if(insert_result.acknowledged):
            print("Successfully inserted into db" + "\n")
            numberOfRecordsAdded += 1
        else:
            print("Failed to store data in db" + "\n")

print("The total number of records added is: " + str(numberOfRecordsAdded))
"""

# Code below uploads all data from hourly_1_room_dataset.csv into mongodb
"""
mydb = myclient["ElectricityApp"]
collection = mydb["test_data"]
data = pd.read_csv('hourly_1_room_dataset.csv')

listOfElecCons = []
data.columns = ["electricity_consumption"]
for i in data["electricity_consumption"]:
    listOfElecCons.append(i)

print(listOfElecCons)

timestamp = datetime.datetime(2010, 1, 1)
for i in range(len(listOfElecCons)):
    if i != 0:
        timestamp = timestamp + datetime.timedelta(hours=1)
    mongoData = {"timestamp": str(timestamp),
                 "electricity_consumption": listOfElecCons[i],
                 "household_id": 1}
    insert_result = collection.insert_one(mongoData)
    if(insert_result.acknowledged):
        print("Successfully inserted into db" + "\n")
    else:
        print("Failed to store data in db" + "\n")
"""


# Load the data from the file 'household_power_consumption.txt' using pandas
# and specify the delimiter as ';'
#data = pd.read_csv('household_power_consumption.txt', delimiter=';')
data = pd.read_csv('household_power_consumption.csv')

# Convert the 'Date' and 'Time' columns to a single 'date_time' column
# by combining the two columns and converting to datetime format
#data['date_time'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

# Convert the 'Global_active_power' column to numeric format
# and remove any rows with NaN values
data['Global_active_power'] = pd.to_numeric(data['Global_active_power'], errors='coerce')
data = data.dropna(subset=['Global_active_power'])

# Convert the 'date_time' column to datetime format
data['date_time'] = pd.to_datetime(data['date_time'])

# Keep only the columns 'date_time', 'Global_active_power'
data = data.loc[:,['date_time','Global_active_power']]

# Sort the data by date_time in ascending order
data.sort_values('date_time', inplace=True, ascending=True)

# Group by hour and calculate sum
data = data.groupby(data['date_time'].dt.floor('H')).sum()

# Reset the index of the data
data = data.reset_index(drop=True)

data.to_csv('hourly_1_room_dataset.csv', index=False)

for i in range(4):
    multiplier = 1.2
    data['Global_active_power'] = data['Global_active_power'] * multiplier 

    # Store the transformed dataset
    file_name = f"hourly_{i+2}_room_dataset.csv"
    data.to_csv(file_name, index=False)
