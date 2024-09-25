#include <Arduino.h>
#include "bmi270.h"
#include "wifi.hpp"

// Create a new sensor object
BMI270 imu;

void setup() {
  Serial.begin(115200);

  //wait for serial to send when doing serial
  //while(!Serial.available());
  setupWifi();
  setupBMI(imu);
  
  LOG_INFO(F("Wait for server"));
  while(!tryConnectServer());

  //start serial stuff
  //Serial.print("Begin\n");
  //printHeader();
}


uint32_t ticks = 0;
time_t startTime = millis();
void loop() {
  //serial output data
  //printSensor(imu);

  sendWifiSensor(imu);
  ticks += 1;

  if (ticks >= 1000) {
    Serial.print("Ticks/s: ");
    Serial.println(1000/((startTime-millis())/ 1000.0));
    ticks = 0;
  }


  

}
