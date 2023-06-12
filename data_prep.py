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
