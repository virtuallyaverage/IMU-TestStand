#include <Arduino.h>
#include "bmi270.h"

// Create a new sensor object
BMI270 imu;

void setup() {
  Serial.begin(115200);
  while(!Serial.available());
  setupBMI(imu);
  
  
  Serial.print("Begin\n");
  printHeader();
}

void loop() {
  printSensor(imu);
  // put your main code here, to run repeatedly:
}
