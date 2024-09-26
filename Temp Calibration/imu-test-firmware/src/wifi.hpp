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

bool sendFloat(WiFiClient &client, SensorPackets packetType, float_t input) {
    if (client) {
        client.write((const char*)&packetType, sizeof(SensorPackets)); // Send the enum value
        client.write((const char*)&input, sizeof(float_t)); // Send the float
        return true;
    } else {
        return false;
    }
}

bool sendTime(WiFiClient &client, SensorPackets packetType, time_t input) {
    float time_float = static_cast<float>(input);
    if (client) {
        client.write((const char*)&packetType, sizeof(SensorPackets)); // Send the enum value
        client.write((const char*)&time_float, sizeof(float_t)); // Send the float
        return true;
    } else {
        return false;
    }
}

bool tryConnectServer() {
    client = server.accept();
    if (client) {
        return client;
    } else {
        return false;
    }
}

void sendWifiSensor(BMI270 &imu) {
    if (!client) {
        if (!tryConnectServer()) {
            LOG_ERROR(F("Server not found"));
            return;
        }
    }

    imu.getSensorData();
    time_t currentTime = millis();
    float temp = 0;
    imu.getTemperature(&temp);

    // Correct buffer size: 8 enums + 8 floats
    uint8_t buffer[(sizeof(SensorPackets) + sizeof(float_t)) * 8];
    uint8_t* ptr = buffer;

    // Add timestamp
    SensorPackets packetType = TIME;
    memcpy(ptr, &packetType, sizeof(SensorPackets));
    ptr += sizeof(SensorPackets);
    float time_float = static_cast<float>(currentTime);
    memcpy(ptr, &time_float, sizeof(float_t));
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

    // Send all data in one go
    client.write(buffer, ptr - buffer);
}
