/*
  ESP32 publish telemetry data to VOne Cloud (Agriculture)
*/

#include "VOneMqttClient.h"
#include "DHT.h"

int MinMoistureValue = 4095;
int MaxMoistureValue = 1800;
int MinMoisture = 0;
int MaxMoisture = 100;
int Moisture = 0;

//define device id
const char* DHT11Sensor = "ff23d012-4452-4f25-b4eb-9a4a83b0bedf";     //Replace with  deviceID for the DHT11 sensor
const char* RainSensor = "31a3d385-648c-451c-a11f-eab97c5093ba";      //Replace with  deviceID for the rain sensor
const char* MoistureSensor = "e86e69e2-5751-4500-983a-3b82ed793cfb";  //Replace with  deviceID for the moisture sensor
const char* WaterLevelSensor = "4fd2c05e-6860-43ef-b064-b80eaf7bbfc1"; // Replace with  ultrasonic sensor deviceID
const char* WaterPump = "2b442c10-2e65-40f2-9072-27da9cf9f93f";   

//Used Pins
const int dht11Pin = 22;
const int rainPin = 35;
const int moisturePin = 34;
const int trigPin = 19;
const int echoPin = 21;
const int relayPin = 32; 

//input sensor
#define DHTTYPE DHT11
DHT dht(dht11Pin, DHTTYPE);

//Create an instance of VOneMqttClient
VOneMqttClient voneClient;

//last message time
unsigned long lastMsgTime = 0;

// Water level thresholds in cm (Early growth state)
const int SafeWaterLevelMin = 4;  // Minimum safe water level
const int SafeWaterLevelMax = 6; // Maximum safe water level

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void setup() {

  setup_wifi();
  voneClient.setup();

  //sensor
  dht.begin();
  pinMode(rainPin, INPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW); // Ensure the pump is off initially

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Serial.begin(115200);
}

// float readWaterLevel() {
//   // Measure distance using ultrasonic sensor
//   digitalWrite(trigPin, LOW);
//   delayMicroseconds(2);
//   digitalWrite(trigPin, HIGH);
//   delayMicroseconds(10);
//   digitalWrite(trigPin, LOW);

//   long duration = pulseIn(echoPin, HIGH);
//   float distance = (duration * 0.034) / 2; // Convert to cm
//   return distance;
// }

void loop() {

  if (!voneClient.connected()) {
    voneClient.reconnect();
    String errorMsg = "DHTSensor Fail";
    voneClient.publishDeviceStatusEvent(DHT11Sensor, true);
    voneClient.publishDeviceStatusEvent(RainSensor, true);
    voneClient.publishDeviceStatusEvent(MoistureSensor, true);
    voneClient.publishDeviceStatusEvent(WaterLevelSensor, true);
    voneClient.publishDeviceStatusEvent(WaterPump, true);
  }
  voneClient.loop();

  unsigned long cur = millis();
  if (cur - lastMsgTime > INTERVAL) {
    lastMsgTime = cur;

    //Publish telemetry data 1
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    JSONVar payloadDHT;
    payloadDHT["Humidity"] = humidity;
    payloadDHT["Temperature"] = temperature;
    voneClient.publishTelemetryData(DHT11Sensor, payloadDHT);

    //Sample sensor fail message
    //String errorMsg = "DHTSensor Fail";
    //voneClient.publishDeviceStatusEvent(DHT22Sensor, false, errorMsg.c_str());

    //Publish telemetry data 2
    int raining = !digitalRead(rainPin);
    voneClient.publishTelemetryData(RainSensor, "Raining", raining);

    //Publish telemetry data 3
    int sensorValue = analogRead(moisturePin);
    Moisture = map(sensorValue, MinMoistureValue, MaxMoistureValue, MinMoisture, MaxMoisture);
    voneClient.publishTelemetryData(MoistureSensor, "Soil moisture", Moisture);

    //  // Publish water level data
    // float waterLevel = readWaterLevel();
    // JSONVar payloadWaterLevel;
    // payloadWaterLevel["Water Level"] = waterLevel;
    // voneClient.publishTelemetryData(WaterLevelSensor, payloadWaterLevel);

     // Read water level from ultrasonic sensor
    long duration;
    float waterLevel;
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    waterLevel = (duration * 0.034) / 2; // Calculate distance in cm

    JSONVar payloadWaterLevel;
    payloadWaterLevel["Depth"] = waterLevel;  // Use Depth if required by V-ONE
    voneClient.publishTelemetryData(WaterLevelSensor, "Water Level", waterLevel);

    // Water pump control logic
    if (!raining && Moisture < 30 && waterLevel < SafeWaterLevelMin) {
      digitalWrite(relayPin, HIGH); // Turn on pump
      voneClient.publishDeviceStatusEvent(WaterPump, true);
      Serial.println("Water pump activated");
    } else if (waterLevel > SafeWaterLevelMax || raining) {
      digitalWrite(relayPin, LOW); // Turn off pump
      voneClient.publishDeviceStatusEvent(WaterPump, false);
      Serial.println("Water pump deactivated");
    }

     // Debugging output
    Serial.println("=== Sensor Readings ===");
    Serial.printf("Temperature: %.1f°C\n", temperature);
    Serial.printf("Humidity: %.1f%%\n", humidity);
    Serial.printf("Rain: %s\n", raining ? "Yes" : "No");
    Serial.printf("Soil Moisture: %d%%\n", Moisture);
    Serial.printf("Water Level: %.1f cm\n", waterLevel);
    Serial.println("=========================");
  }
}
