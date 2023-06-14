import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

#Average monthly household electricity consumption by dwelling type (in kWh), source: https://www.ema.gov.sg/statistic.aspx?sta_sid=20140617E32XNb1d0Iqa
housing_df = pd.read_csv('total_household_electricity_consumption_2005_2020.csv')

def convertfloat(x):
    x['overall'] = x['overall'].astype(float)
    x['public_housing'] = x['public_housing'].astype(float)
    x['1-room_2-room'] = x['1-room_2-room'].astype(float)
    x['3-room'] = x['3-room'].astype(float)
    x['4-room'] = x['4-room'].astype(float)
    x['5-room_and_executive'] = x['5-room_and_executive'].astype(float)
    x['private_housing'] = x['private_housing'].astype(float)
    x['private_apts_and_condo'] = x['private_apts_and_condo'].astype(float)
    x['landed_properties'] = x['landed_properties'].astype(float)
    x['others'] = x['others'].astype(float)
    return x

housing_df = housing_df.sort_values(by = ['month'], ascending = True)
housing_df = convertfloat(housing_df)
housing_df = housing_df.rename(columns = {'public_housing': 'public_housing_total', 'private_housing': 'private_housing_total'})

#housing_df_month = housing_df.copy()
#housing_df_dwelling_type = housing_df.copy()

consumption_data = housing_df ['5-room_and_executive'].values

#scaler = MinMaxScaler(feature_range=(0, 1))
#normalized_data = scaler.fit_transform(consumption_data.reshape(-1, 1))


def create_sequences(data, sequence_length):
    X = []
    y = []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i+sequence_length])
        y.append(data[i+sequence_length])
    return np.array(X), np.array(y)

sequence_length = 10  # Number of previous time steps to consider
X, y = create_sequences(consumption_data, sequence_length)

train_ratio = 0.8  # Percentage of data to use for training
train_size = int(len(X) * train_ratio)

X_train = X[:train_size]
y_train = y[:train_size]
X_test = X[train_size:]
y_test = y[train_size:]

model = Sequential()
model.add(LSTM(64, input_shape=(sequence_length, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(X_train, y_train, epochs=50, batch_size=30)

mse = model.evaluate(X_test, y_test)
print("Mean Squared Error:", mse)

predictions = model.predict(X_test)
#print(X_test)
print(predictions)
#print(predictions.shape)


