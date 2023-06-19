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
predictions = []

# Get all records from listOfHouseholdID in Electricity collection
mydb = myclient["Hougang-Electric"]
collection = mydb["Electricity"]
#mydb = myclient["Hougang-Electric"]
#collection = mydb["query_elec"]
query = {"household_id": {"$in": listOfHouseholdID}}
result = collection.find(query)

df = pd.DataFrame(list(result))
dataset = df.tail(50)
dataset['electricity_consumption'] = pd.to_numeric(dataset['electricity_consumption'], errors='coerce')
dataset = dataset['electricity_consumption'].tolist()

model_name = f"1_room_model.h5"
model = keras.models.load_model(model_name)

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=48):
    X = []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
    return np.array(X)

for i in range(24):
    
    #Reshape the numpy array into a 2D array with 1 column
    dataset = np.reshape(dataset[:], (-1, 1))

    #Create an instance of the MinMaxScaler class to scale the values between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))

    #Fit the MinMaxScaler to the transformed data and transform the values
    dataset = scaler.fit_transform(dataset)

    # reshape into X=t and Y=t+1
    look_back = 48
    X_test = create_dataset(dataset, look_back)

    # reshape input to be [samples, time steps, features]
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # make predictions
    test_predict = model.predict(X_test)

    # invert predictions
    prediction = scaler.inverse_transform(test_predict)

    predictions.append(prediction[-1])

    dataset = scaler.inverse_transform(dataset)
    dataset = np.append(dataset, prediction[-1])

predictions = [arr.flatten()[0] for arr in predictions]
print(predictions)
    