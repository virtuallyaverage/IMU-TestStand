#pragma once

#include <ESP8266WiFi.h>
#include "SparkFun_BMI270_Arduino_Library.h"

#include "config.h"
#include "DebugLog.h"

WiFiServer server(80);
WiFiClient client;

bool setupWifi() {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    LOG_DEBUG(F("Connecting Wifi"));
    while (WiFi.status() != WL_CONNECTED) {
        delay(10);
    }
    LOG_DEBUG(F("Wifi Connected: "), WiFi.localIP().toString());

    // start wifiserver
    server.begin();
    return true;
}

bool sendFloat(WiFiClient &client, float_t input) {
    if (client) {
        client.write((const char*)&input, sizeof(float_t));
        return true;
    } else {
        return false;
    }
}

bool sendFloatWithID(WiFiClient &client, SensorPackets id, float_t input) {
    if (client) {
        cclient.write((const char*)&packetType, sizeof(SensorPackets)); // Send the enum value
        client.write((const char*)&input, sizeof(float_t)); // Send the float
        return true;
    } else {
        return false;
    }
}

bool sendTime(WiFiClient &client, time_t input) {
    float time_float = static_cast<float>(input);
    if (client) {
        client.write(reinterpret_cast<const char*>(&time_float), sizeof(float));
        return true;
    }
    return false;
}

enum SensorPackets {
    TIME,
    TEMP,
    ACCX,
    ACCY,
    ACCZ,
    GYROX,
    GYROY,
    GYROZ
}

void sendWifiSensor(BMI270 &imu) {
    if (!client) {
        LOG_ERROR(F("Server not found"));
        return;
    }

    // the sensor data, otherwise it will never update
    imu.getSensorData();
    time_t currentTime = millis();

    // fill temp with temperature
    float temp = 0;
    imu.getTemperature(&temp);

    //timestamp
    sendTime(client, currentTime);

    //send temperature
    sendFloat(client, temp);

    //Linear Accel
    sendFloat(client, imu.data.accelX);
    sendFloat(client, imu.data.accelY);
    sendFloat(client, imu.data.accelZ);

    //Gyro Rate
    sendFloat(client, imu.data.gyroX);
    sendFloat(client, imu.data.gyroX);
    sendFloat(client, imu.data.gyroZ);
}

bool tryConnectServer() {
    client = server.accept();
    if (client) {
        return client;
    } else {
        return false;
    }
}