import keras

import pandas as pd

import numpy as np

# Import MinMaxScaler from sklearn
from sklearn.preprocessing import MinMaxScaler

for i in range(5):
    
    file_name = f"hourly_{i+1}_room_dataset.csv"
    data = pd.read_csv(file_name)

    model_name = f"{i+1}_room_model.h5"
    model = keras.models.load_model(model_name)

    #Transform the Global_active_power column of the data DataFrame into a numpy array of float values
    dataset = data.Global_active_power.values.astype('float32')

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
    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            X.append(a)
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)

    # reshape into X=t and Y=t+1
    look_back = 24
    X_test, Y_test = create_dataset(test, look_back)

    # reshape input to be [samples, time steps, features]
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # make predictions
    test_predict = model.predict(X_test)

    # invert predictions
    test_predict = scaler.inverse_transform(test_predict)

    print(test_predict[-5])