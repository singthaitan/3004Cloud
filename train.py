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

# Import preprocessing from sklearn
import sklearn
from sklearn import preprocessing

# Import necessary functions from keras
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import *

# Import MinMaxScaler from sklearn
from sklearn.preprocessing import MinMaxScaler

# Import mean squared error and mean absolute error from sklearn
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# Import early stopping from keras callbacks
from keras.callbacks import EarlyStopping

# Import MongoDB
import pymongo
import pandas as pd
import datetime
import numpy as np

# Getting all household id and storing it into a dictionary based on household type
def getAllHouseholdID(household_type):
    # Create an empty dictionary that stores each room type household ids
    roomTypeDict = {"1 Room": [],
                "2 Room": [],
                "3 Room": [],
                "4 Room": [],
                "5 Room": [],}
    
    # Query from Household collection
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

# Populating mongodb with records
def insertDataFromCsv(filename, listOfID, numberOfData):
    # Select the Electricity collection from mongodb
    mydb = myclient["Hougang-Electric"]
    collection = mydb["Electricity"]
    # Retrieve file and number of records needed
    data = pd.read_csv(filename, nrows=numberOfData)

    # Storing csv data into a list
    listOfElecCons = []
    data.columns = ["electricity_consumption"]
    for i in data["electricity_consumption"]:
        listOfElecCons.append(i)

    # timestamp = datetime.datetime(2023, 4, 1)
    numberOfRecordsAdded = 0
    numberOfHouseholds = len(listOfID)
    sublists = np.array_split(listOfElecCons, numberOfHouseholds)
    print(sublists)
    for i in range(len(sublists)):
        timestamp = datetime.datetime(2023, 4, 1)
        for y in range(len(sublists[i])):
            print(sublists[i][y])
            if y != 0:
                timestamp = timestamp + datetime.timedelta(hours=1)
            mongoData = {"timestamp": str(timestamp),
                        "electricity_consumption": sublists[i][y],
                        "household_id": listOfID[i]}
            insert_result = collection.insert_one(mongoData)
            if(insert_result.acknowledged):
                print("Successfully inserted into db" + "\n")
                numberOfRecordsAdded += 1
            else:
                print("Failed to store data in db" + "\n")

    print("The total number of records added is: " + str(numberOfRecordsAdded))

# Set up Mongodb Atlas
myclient = pymongo.MongoClient("mongodb+srv://shawn:shawn@app-cluster.zxcw8od.mongodb.net/")
mydb = myclient["Hougang-Users"]
collection = mydb["Household"]

# Get household ID based on household type
listOfHouseholdID = getAllHouseholdID("1 Room")
dataset = []

# Get all records from listOfHouseholdID in electricity_consumption collection
mydb = myclient["Hougang-Electric"]
collection = mydb["Electricity"]
query = {"household_id": {"$in": listOfHouseholdID}}
result = collection.find(query)


# Uncomment code below if uploading data into mongodb

# Inserting records from all 5 csvs into database
"""
for roomNo in range(1, 6):
    listOfID = getAllHouseholdID(str(roomNo) + " Room")
    # for i in listOfID:
    #     print(i)
    insertDataFromCsv("hourly_" + str(roomNo) +"_room_dataset.csv", listOfID, 10)
"""


# Code below uploads all data from hourly_5_room_dataset.csv into mongodb
"""
listOfID = getAllHouseholdID("5 Room")
insertDataFromCsv("hourly_5_room_dataset.csv", listOfID, 11)
"""

# Convert the 'Global_active_power' column to numeric format
# and remove any rows with NaN values
for row in result:
    timestamp = row["timestamp"]
    electricity_consumption = row["electricity_consumption"]
    # print("The timestamp is: " + timestamp + "\n" + "The electricity consumption is: " + str(electricity_consumption) + "\n")
    # print(row)

    row['electricity_consumption'] = pd.to_numeric(row['electricity_consumption'], errors='coerce')

    # Convert the 'date_time' column to datetime format
    row['timestamp'] = pd.to_datetime(row['timestamp'])

    #Transform the Global_active_power column of the data DataFrame into a numpy array of float values
    dataset.append(row["electricity_consumption"])

#Reshape the numpy array into a 2D array with 1 column
dataset = np.reshape(dataset, (-1, 1))

#Create an instance of the MinMaxScaler class to scale the values between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))

#Fit the MinMaxScaler to the transformed data and transform the values
dataset = scaler.fit_transform(dataset)

#Split the transformed data into a training set (80%) and a test set (20%)
train_size = int(len(dataset) * 0.80)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=48):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

# reshape into X=t and Y=t+1
look_back = 48
X_train, Y_train = create_dataset(train, look_back)
X_test, Y_test = create_dataset(test, look_back)


# reshape input to be [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# Defining the LSTM model
model = Sequential()

# Adding the first layer with 100 LSTM units and input shape of the data
model.add(LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])))

# Adding a dropout layer to avoid overfitting
model.add(Dropout(0.2))

# Adding a dense layer with 1 unit to make predictions
model.add(Dense(1))

# Compiling the model with mean squared error as the loss function and using Adam optimizer
model.compile(loss='mean_squared_error', optimizer='adam')

# Fitting the model on training data and using early stopping to avoid overfitting
history = model.fit(X_train, Y_train, epochs=20, batch_size=24, validation_data=(X_test, Y_test), 
                    callbacks=[EarlyStopping(monitor='val_loss', patience=4)], verbose=1, shuffle=False)

# make predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# invert predictions
train_predict = scaler.inverse_transform(train_predict)
Y_train = scaler.inverse_transform([Y_train])
test_predict = scaler.inverse_transform(test_predict)
Y_test = scaler.inverse_transform([Y_test])

print('Train Mean Absolute Error:', mean_absolute_error(Y_train[0], train_predict[:,0]))
print('Train Root Mean Squared Error:',np.sqrt(mean_squared_error(Y_train[0], train_predict[:,0])))
print('Test Mean Absolute Error:', mean_absolute_error(Y_test[0], test_predict[:,0]))
print('Test Root Mean Squared Error:',np.sqrt(mean_squared_error(Y_test[0], test_predict[:,0])))

model_name = f"5_room_model.h5"
#model.save(model_name)
