#include "bmi270.h"


bool setupBMI(BMI270 &imu)
{
    // Initialize the I2C library
    Wire.begin();

    bool result = false;

    bool connected = false;
    while (!connected) {
        // Check if sensor is connected and initialize
        if (imu.beginI2C(BMI2_I2C_PRIM_ADDR, Wire) == BMI2_OK) {
            LOG_INFO(F("IMU found on primary address"));
            result = true;
            connected = true;
        } else if (imu.beginI2C(BMI2_I2C_SEC_ADDR, Wire) == BMI2_OK) {
            LOG_INFO(F("IMU found on secondary address"));
            result = true;
            connected = true;
        } else {
            LOG_ERROR(F("no IMU Found"));
            result = false;
        }
        delay(500);
    }
    processConfigError(setAccConfig(imu));
    processConfigError(setGyroConfig(imu));

    imu.disableAdvancedPowerSave();


    return result;

}

int8_t setAccConfig(BMI270 &imu) {
    int8_t err = BMI2_OK;

    // Set accelerometer config
    bmi2_sens_config accelConfig;
    accelConfig.type = BMI2_ACCEL;
    accelConfig.cfg.acc.odr = BMI2_ACC_ODR_100HZ;
    accelConfig.cfg.acc.bwp = BMI2_ACC_OSR2_AVG2; //lower gives higher frequency
    accelConfig.cfg.acc.filter_perf = BMI2_PERF_OPT_MODE;
    accelConfig.cfg.acc.range = BMI2_ACC_RANGE_16G;
    err = imu.setConfig(accelConfig);
    return err;
}

int8_t setGyroConfig(BMI270 &imu) {
    int8_t err = BMI2_OK;

    // Set gyroscope config
    bmi2_sens_config gyroConfig;
    gyroConfig.type = BMI2_GYRO;
    gyroConfig.cfg.gyr.odr = BMI2_GYR_ODR_400HZ;
    gyroConfig.cfg.gyr.bwp = BMI2_GYR_OSR2_MODE;//lower gives higher frequency
    gyroConfig.cfg.gyr.filter_perf = BMI2_PERF_OPT_MODE;
    gyroConfig.cfg.gyr.ois_range = BMI2_GYR_OIS_250;
    gyroConfig.cfg.gyr.range = BMI2_GYR_RANGE_1000;
    gyroConfig.cfg.gyr.noise_perf = BMI2_PERF_OPT_MODE;
    err = imu.setConfig(gyroConfig);
    return err;
}

void processConfigError(int8_t err) {
    // Not valid, determine which config was the problem
    if(err == BMI2_E_ACC_INVALID_CFG)
    {
        LOG_ERROR(F("Accelerometer config not valid!"));
    }
    else if(err == BMI2_E_GYRO_INVALID_CFG)
    {
        LOG_ERROR(F("Gyroscope config not valid!"));
    }
    else if(err == BMI2_E_ACC_GYR_INVALID_CFG)
    {
        LOG_ERROR(F("Both configs not valid!"));
    }
    else
    {
        LOG_ERROR(F("Unknown error: "));
        Serial.println(err);
    }
}

void printHeader() {
    Serial.print("Temp,");
    Serial.print("AccelX,");
    Serial.print("AccelY,");
    Serial.print("AccelZ,");
    Serial.print("GyroX,");
    Serial.print("GyroY,");
    Serial.print("GyroZ,");
    Serial.print("Millis,\n");
}

void printSensor(BMI270 &imu)
{
    // Get measurements from the sensor. This must be called before accessing
    // the sensor data, otherwise it will never update
    imu.getSensorData();
    time_t currentTime = millis();

    // fill temp with temperature
    float temp = 0;
    imu.getTemperature(&temp);

    Serial.print(temp);
    Serial.print(",");

    // Print acceleration data
    Serial.print(imu.data.accelX, 5);
    Serial.print(",");
    Serial.print(imu.data.accelY, 5);
    Serial.print(",");
    Serial.print(imu.data.accelZ, 5);
    Serial.print(",");

    // Print rotation data
    Serial.print(imu.data.gyroX, 5);
    Serial.print(",");
    Serial.print(imu.data.gyroY, 5);
    Serial.print(",");
    Serial.print(imu.data.gyroZ, 5);
    Serial.print(",");

    //print time of measurement
    Serial.print(currentTime);
    Serial.print(",\n");

}