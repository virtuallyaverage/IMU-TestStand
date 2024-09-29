#pragma once

#include <ESP8266WiFi.h>
#include "SparkFun_BMI270_Arduino_Library.h"

#include "config.h"
#include "DebugLog.h"
#include "profile.h"

WiFiServer server(80);
WiFiClient client;

enum SensorPackets {
    TIME,
    TEMP,
    ACCX,
    ACCY,
    ACCZ,
    GYROX,
    GYROY,
    GYROZ
};

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

bool tryConnectServer() {
    client = server.accept();
    if (client) {
        return client;
    } else {
        return false;
    }
}

// Adjust buffer size to accommodate BUNDLE_SIZE readings
uint8_t buffer[(sizeof(SensorPackets) + sizeof(float_t)) * 8 * BUNDLE_SIZE];
uint8_t* ptr = buffer;
int readingsCount = 0;

void sendDataToClient(WiFiClient &client, uint8_t *buffer, size_t size) {
    if (client) {
        client.write(buffer, size);
    } else {
        LOG_ERROR(F("Client not connected"));
    }
}

void addSensorDataToBuffer(uint8_t*& ptr, SensorPackets packetType, float value) {
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &value, sizeof(float_t));
    ptr += sizeof(float_t);
}

void addTimestampToBuffer(uint8_t*& ptr) {
    time_t currentTime = millis();
    SensorPackets packetType = TIME;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &currentTime, sizeof(float_t));
    ptr += sizeof(float_t);
}

void TickWifiSensor(BMI270 &imu) {
    if (!client) {
        if (!tryConnectServer()) {
            LOG_ERROR(F("Server not found"));
            return;
        }
    }

    imu.getSensorData();
    float temp = 0;
    imu.getTemperature(&temp);

    // Add timestamp
    addTimestampToBuffer(ptr);

    // Add temperature
    addSensorDataToBuffer(ptr, TEMP, temp);

    // Add accelerometer data
    addSensorDataToBuffer(ptr, ACCX, imu.data.accelX);
    addSensorDataToBuffer(ptr, ACCY, imu.data.accelY);
    addSensorDataToBuffer(ptr, ACCZ, imu.data.accelZ);

    // Add gyro data
    addSensorDataToBuffer(ptr, GYROX, imu.data.gyroX);
    addSensorDataToBuffer(ptr, GYROY, imu.data.gyroY);
    addSensorDataToBuffer(ptr, GYROZ, imu.data.gyroZ);

    readingsCount++;

    // Send data if BUNDLE_SIZE is reached
    if (readingsCount >= BUNDLE_SIZE) {
        sendDataToClient(client, buffer, ptr - buffer);
        ptr = buffer; // Reset pointer
        readingsCount = 0; // Reset count
    }
}