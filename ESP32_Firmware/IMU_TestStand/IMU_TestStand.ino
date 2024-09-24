#include <WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";
WiFiUDP udp;
const char* udpAddress = "PC_IP_ADDRESS";
const uint16_t udpPort = 12345;

#define IMU_SDA 21
#define IMU_SCL 22
#define I2C_ADDRESS 0x3C // IMU I2C address


void setup() {
  Serial.begin(115200);
  
  //connect to sensor
  Wire.setPins(IMU_SDA, IMU_SCL);
  Wire.begin(); 
  //setup settings
  Wire.beginTransmission(BMI160_ADDRESS);
  Wire.write(0x7E); // Select command register
  Wire.write(0x11); // Set accelerometer and gyroscope to normal mode
  Wire.endTransmission();

  //connect to wifi
  WiFi.begin(ssid, password);
  while (WiFi.status()!= WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

void loop() {
  float value1 = 1.23;
  float value2 = 4.56;
  udp.beginPacket(udpAddress, udpPort);
  udp.write((byte*)&value1, sizeof(value1));
  udp.write((byte*)&value2, sizeof(value2));
  udp.endPacket();
  delay(1000); // Adjust delay as needed
}
