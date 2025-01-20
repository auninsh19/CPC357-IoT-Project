# Start your code below, you can access parameter values as normal list starting from index 1 e.g. i = parameter[1], you can write to output value as normal list starting from index 1 e.g. output[1]= 1+1

obj = parameter[1]["data"]
arrlgt = parameter[1]["count"]["total"] - 1
rain_value = obj[arrlgt]["Rain"]  # Assuming the rain sensor data is stored under "Rain"
threshold = 500  # Adjust this threshold value based on your rain sensor data range

# Check if the rain value indicates "rain"
if int(rain_value) < threshold:  # If the value is below the threshold, it indicates rain (assuming low value means rain detected)
    msgbody = '<p>The current rain status is "Raining". Irrigation paused to conserve water. The rain sensor reading is ' + rain_value + '.</p><br>'
    output[1] = "[Warning] Rain Detected!"
    output[2] = msgbody
    output[3] = 2  # Indicating a warning condition

elif int(rain_value) >= threshold:  # If the value is above the threshold, it indicates no rain
    msgbody = '<p>The current rain status is "No Rain". The rain sensor reading is ' + rain_value + '.</p><br>'
    output[1] = "[Info] No Rain Detected."
    output[2] = msgbody
    output[3] = 1  # Indicating normal condition (no rain)

# end your code here #
