import keras

import pandas as pd

import numpy as np

# Import warnings and set filter to ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Import MinMaxScaler from sklearn
from sklearn.preprocessing import MinMaxScaler

# Import MongoDB
import pymongo

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

# Set up Mongodb Atlas
myclient = pymongo.MongoClient("mongodb+srv://shawn:shawn@app-cluster.zxcw8od.mongodb.net/")
mydb = myclient["Hougang-Users"]
collection = mydb["Household"]

# Get household ID based on household type
listOfHouseholdID = getAllHouseholdID("1 Room")
dataset = []

# Get all records from listOfHouseholdID in Electricity collection
mydb = myclient["Hougang-Electric"]
collection = mydb["Electricity"]
query = {"household_id": {"$in": listOfHouseholdID}}
result = collection.find(query)
df = pd.DataFrame(list(result))
dataset = df.tail(73)
dataset['electricity_consumption'] = pd.to_numeric(dataset['electricity_consumption'], errors='coerce')
dataset = dataset['electricity_consumption'].tolist()

'''
# Print records retrieved from database based from household type
for row in result:
    timestamp = row["timestamp"]
    electricity_consumption = row["electricity_consumption"]
    #print("The timestamp is: " + timestamp + "\n" + "The electricity consumption is: " + str(electricity_consumption) + "\n")
    #print(row)

    row['electricity_consumption'] = pd.to_numeric(row['electricity_consumption'], errors='coerce')

    dataset.append(row["electricity_consumption"])

'''

model_name = f"1_room_model.h5"
model = keras.models.load_model(model_name)

#Reshape the numpy array into a 2D array with 1 column
dataset = np.reshape(dataset, (-1, 1))

#Create an instance of the MinMaxScaler class to scale the values between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))

#Fit the MinMaxScaler to the transformed data and transform the values
dataset = scaler.fit_transform(dataset)

#Split the transformed data into a training set (80%) and a test set (20%)
#train_size = int(len(dataset) * 0.80)
#test_size = len(dataset) - train_size
#train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

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
X_test, Y_test = create_dataset(dataset, look_back)

# reshape input to be [samples, time steps, features]
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# make predictions
test_predict = model.predict(X_test)

# invert predictions
test_predict = scaler.inverse_transform(test_predict)

print(test_predict[:,0])
