#pragma once

#include <Wire.h>
#include "SparkFun_BMI270_Arduino_Library.h"
#include <DebugLog.h>

#define CONFIGS (BMI2_ACCEL, BMI2_GYRO, BMI2_AUX, BMI2_GYRO_GAIN_UPDATE, BMI2_ANY_MOTION, BMI2_NO_MOTION, BMI2_SIG_MOTION, BMI2_STEP_COUNTER_PARAMS, BMI2_STEP_DETECTOR, BMI2_STEP_COUNTER, BMI2_STEP_ACTIVITY, BMI2_WRIST_GESTURE, BMI2_WRIST_WEAR_WAKE_UP);

bool setupBMI(BMI270 &imu);
void printSensor(BMI270 &imu);
void printHeader();

int8_t setAccConfig(BMI270 &imu);
int8_t setGyroConfig(BMI270 &imu);
void processConfigError(int8_t err);