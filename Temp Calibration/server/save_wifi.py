import csv
import json
import struct
import os
import socket
from enum import IntEnum

class SensorPackets(IntEnum):
    TIME = 0
    TEMP = 1
    ACCX = 2
    ACCY = 3
    ACCZ = 4
    GYROX = 5
    GYROY = 6
    GYROZ = 7

def recieve_data(host, port, num_sensors):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        sensor_data = {}
        for _ in range(num_sensors):
            id_bytes = s.recv(4)  # Assuming 4-byte enum
            packet_type = SensorPackets(struct.unpack('<I', id_bytes)[0])
            data = s.recv(4)  # Receive 4 bytes for the float
            if len(data) < 4:
                raise ValueError("Incomplete data received")
            float_value = struct.unpack('<f', data)[0]  # '<f' for little-endian float
            sensor_data[packet_type] = float_value
        return sensor_data
                
if __name__ == "__main__":
    file_name = "v1_wifi"
    save_file_path = os.path.join("data", "bmi270", "static", file_name + ".csv")

    with open("config.json", "r") as file:
        config = json.load(file)
        
    print(save_data(config["ip"], config["wifi_port"], save_file_path))