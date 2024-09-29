import json
import struct
import os
import socket
from enum import IntEnum
from time import time

class SensorPackets(IntEnum):
    TIME = 0
    TEMP = 1
    ACCX = 2
    ACCY = 3
    ACCZ = 4
    GYROX = 5
    GYROY = 6
    GYROZ = 7

BUNDLE_SIZE = 100  # Define the bundle size to match the sender

def receive_continuous(host, port):
    #init profiling 
    readings = 0
    start = time()
    
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            #display readings per second
            if readings >= BUNDLE_SIZE:
                now = time()
                diff = now-start
                print(f"Readings Per second: {BUNDLE_SIZE/diff}") # readings / second
                start = now
                readings = 0
            
            # Calculate the total size of the data packet for BUNDLE_SIZE readings
            single_reading_size = (4 + 4) * len(SensorPackets)  # 4 bytes for enum + 4 bytes for float/int
            packet_size = single_reading_size * BUNDLE_SIZE
            data = b''
            
            # Loop to receive the complete data packet
            while len(data) < packet_size:
                packet_part = s.recv(packet_size - len(data))
                if not packet_part:
                    raise ValueError("Connection closed by the server")
                data += packet_part
            
            offset = 0
            for _ in range(BUNDLE_SIZE):
                sensor_data = [0] * len(SensorPackets)
                for packet_type in SensorPackets:
                    # Unpack the enum
                    packet_id = struct.unpack_from('<I', data, offset)[0]
                    offset += 4

                    # Unpack the float/int value
                    if packet_type == SensorPackets.TIME:
                        float_value = struct.unpack_from('<I', data, offset)[0]
                    else:
                        float_value = struct.unpack_from('<f', data, offset)[0]
                    offset += 4

                    sensor_data[packet_type.value] = float_value
                    
                readings += 1 

            

if __name__ == "__main__":
    file_name = "v1_wifi"
    save_file_path = os.path.join("data", "bmi270", "static", file_name + ".csv")

    with open("config.json", "r") as file:
        config = json.load(file)

    receive_continuous(config["ip"], config["wifi_port"])