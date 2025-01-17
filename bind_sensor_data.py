import pandas as pd
import os

# Set the working directory
path = "/Users/auninasuha/Documents/USM/SEM 7/CPC357/Project/Dataset"
os.chdir(path)

# Load each CSV file into a DataFrame
moisture_data = pd.read_csv("Moisture_sensor_data.csv")
rain_data = pd.read_csv("Rain_sensor_data.csv")
dht11_data = pd.read_csv("DHT11_data.csv")

# Drop the 'Device ID' and 'Device Name' columns if they exist
moisture_data = moisture_data.drop(columns=["device_id", "device_name"], errors="ignore")
rain_data = rain_data.drop(columns=["device_id", "device_name"], errors="ignore")
dht11_data = dht11_data.drop(columns=["device_id", "device_name"], errors="ignore")

# Display the resulting DataFrames
print("Moisture Data:")
print(moisture_data.head())

print("\nRain Data:")
print(rain_data.head())

print("\nDHT11 Data:")
print(dht11_data.head())

# Merge the data on the common 'Timestamp' column
merged_data = pd.merge(moisture_data, rain_data, on="insertion_timestamp")
merged_data = pd.merge(merged_data, dht11_data, on="insertion_timestamp")

# Save the merged dataset to a new CSV file
merged_data.to_csv("Merged_sensor_data.csv", index=False)

# Display the first few rows of the merged dataset
print(merged_data.head())

print("Merged data has been saved to 'Merged_sensor_data.csv'.")

