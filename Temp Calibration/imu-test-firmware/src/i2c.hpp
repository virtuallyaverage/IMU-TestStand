#include <Arduino.h>
#include <Wire.h>

bool setupI2C() {
    Wire.begin(0x68);
    Serial.print("Available: ");
    Serial.println(Wire.available());
    
    Serial.print("Status: ");
    Serial.println(Wire.status());
    return true;
}