# CPC357-IoT-Project Smart Agriculture
This project is built to facilitate farmers, particularly paddy farmers to automate irrigation system and to wisely plan when to plant and harvest paddy according to weather forecast feature. 

## Why paddy? 
Malaysia has been facing problem with shortage supply of rice due to several factors, like extreme weather conditions, inefficient water management and inadequate soil nutrient. This project aims to tackle this problem by providing weather forecast feature and automated irrigation system based on sensor data.

Not to mention, this project aligns with United Nation SDG 2 (Zero Hunger), to achieve sustainable food production and ensure sufficient food supply all year around.

## Hardware Components
This project involves hardware components like:
  1. DHT11 - To monitor temperature and humidity of the environment
  2. Moisture sensor - To measure the moisture level of soil
  3. Rain sensor - To measure the presence of rain
  4. Ultrasonic sensor - To measure the water depth of paddy field
  5. Water pump - To demonstrate irrigation system
  6. Relay module - To control water pump
  7. Breadboard and jumper wire

## Software Used
For software, this project use 
  1. V-One platform - For data aggregation, data visualisation, data analysis, and machine learning deployment.
  2. Arduino IDE and necessary libraries - To integrate hardware components with V-One platform.
  3. Python and necessary libraries - For data preprocessing and machine learning model development.

## Dataset Preparation
As for the dataset, the dataset from each sensor are bind together into one dataset named Merged_sensor_data.csv by running bind_sensor_data.py. Some of the columns insignificant for training machine learning model were dropped like device_id and device_name. Then, Merged_sensor_data.csv is used for training machine learning model, specifically Random Forest Classifier, locally (predict_weather_conditions.py) to get the desired dataset with an additional column Weather Condition, and saved as paddy_sensor_data.csv. This step is to prepare the data before uploading the data into V-One for machine learning deployment.
