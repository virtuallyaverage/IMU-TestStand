#pragma once

#include <ESP8266WiFi.h>
#include "SparkFun_BMI270_Arduino_Library.h"

#include "config.h"
#include "DebugLog.h"

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

void sendWifiSensor(BMI270 &imu) {
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
    time_t currentTime = millis();
    SensorPackets packetType = TIME;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &currentTime, sizeof(float_t));
    ptr += sizeof(float_t);

    // Add temperature
    packetType = TEMP;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &temp, sizeof(float_t));
    ptr += sizeof(float_t);

    // Add accelerometer data
    packetType = ACCX;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &imu.data.accelX, sizeof(float_t));
    ptr += sizeof(float_t);

    packetType = ACCY;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &imu.data.accelY, sizeof(float_t));
    ptr += sizeof(float_t);

    packetType = ACCZ;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &imu.data.accelZ, sizeof(float_t));
    ptr += sizeof(float_t);

    // Add gyro data
    packetType = GYROX;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &imu.data.gyroX, sizeof(float_t));
    ptr += sizeof(float_t);

    packetType = GYROY;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &imu.data.gyroY, sizeof(float_t));
    ptr += sizeof(float_t);

    packetType = GYROZ;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    memcpy(ptr, &imu.data.gyroZ, sizeof(float_t));
    ptr += sizeof(float_t);

    readingsCount++;

    // Send data if BUNDLE_SIZE is reached
    if (readingsCount >= BUNDLE_SIZE) {
        client.write(buffer, ptr - buffer);
        ptr = buffer; // Reset pointer
        readingsCount = 0; // Reset count
    }
}