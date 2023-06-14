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

# Set up Mongodb Atlas
myclient = pymongo.MongoClient("mongodb+srv://shawn:shawn@app-cluster.zxcw8od.mongodb.net/")
mydb = myclient["ElectricityApp"]
collection = mydb["Household"]

# Get household ID based on household type
listOfHouseholdID = []
query = {"household_type": 1}
cursor = collection.find(query)
for document in cursor:
    household_id = document["household_id"]
    listOfHouseholdID.append(household_id)

# Get all records from listOfHouseholdID in electricity_consumption collection
collection = mydb["test_data"]
query = {"household_id": {"$in": listOfHouseholdID}}
result = collection.find(query)
dataset = []

for row in result:
    timestamp = row["timestamp"]
    electricity_consumption = row["electricity_consumption"]
    # print("The timestamp is: " + timestamp + "\n" + "The electricity consumption is: " + str(electricity_consumption) + "\n")
    #print(row)

# Load the data from the file 'household_power_consumption.txt' using pandas
# and specify the delimiter as ';'
#data = pd.read_csv('household_power_consumption.txt', delimiter=';')
#data = pd.read_csv('household_power_consumption.csv')

# Convert the 'Date' and 'Time' columns to a single 'date_time' column
# by combining the two columns and converting to datetime format
#data['date_time'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

# Convert the 'Global_active_power' column to numeric format
# and remove any rows with NaN values
    row['electricity_consumption'] = pd.to_numeric(row['electricity_consumption'], errors='coerce')
#row = row.dropna(subset=['electricity_consumption'])

# Convert the 'date_time' column to datetime format
    row['timestamp'] = pd.to_datetime(row['timestamp'])

# Keep only the columns 'date_time', 'Global_active_power'
#row = row.loc[:,['timestamp','electricity_consumption']]

# Sort the data by date_time in ascending order
#row.sort_values('timestamp', inplace=True, ascending=True)

# Group by hour and calculate sum
#row = row.groupby(row['date_time'].dt.floor('H')).sum()

# Reset the index of the data
#row = row.reset_index(drop=True)

#data.to_csv('hourly_1_room_dataset.csv', index=False)

#file_name = f"hourly_{i+1}_room_dataset.csv"
#data = pd.read_csv(file_name)

#Transform the Global_active_power column of the data DataFrame into a numpy array of float values
    dataset.append(row["electricity_consumption"])

#Reshape the numpy array into a 2D array with 1 column
dataset = np.reshape(dataset, (-1, 1))
print(dataset.shape)

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
print(X_train.shape)

# Defining the LSTM model
model = Sequential()

# Adding the first layer with 100 LSTM units and input shape of the data
model.add(LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])))
#model.add(LSTM(64, activation='relu'))

# Adding a dropout layer to avoid overfitting
model.add(Dropout(0.2))

# Adding a dense layer with 1 unit to make predictions
model.add(Dense(24))

# Compiling the model with mean squared error as the loss function and using Adam optimizer
model.compile(loss='mean_squared_error', optimizer='adam')

# Fitting the model on training data and using early stopping to avoid overfitting
history = model.fit(X_train, Y_train, epochs=20, batch_size=24, validation_data=(X_test, Y_test), 
                    callbacks=[EarlyStopping(monitor='val_loss', patience=4)], verbose=1, shuffle=False)

# Displaying a summary of the model
#model.summary()

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

print(test_predict[-5])

model_name = f"1_room_model.h5"
model.save(model_name)