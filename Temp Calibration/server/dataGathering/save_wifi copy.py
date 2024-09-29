import json
import struct
import os
import socket
from enum import IntEnum
import csv

class SensorPackets(IntEnum):
    TIME = 0
    TEMP = 1
    ACCX = 2
    ACCY = 3
    ACCZ = 4
    GYROX = 5
    GYROY = 6
    GYROZ = 7

class wifiBoard():
    def __init__(self, ip, port) -> None:
        self.port = port
        self.ip = ip
        self.board = None
        self.packet_size = (4 + 4) * len(SensorPackets)  # 4 bytes for enum + 4 bytes for float/int
        self.stopWriting = True

    def connect(self):
        self.board = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.board.connect((self.ip, self.port))
        if self.board:
            return True
        return False
             
    def get_line(self):
        sensor_data = [0] * len(SensorPackets)
        offset = 0
        # empty packet
        data = b''
        
        if (self.board == None):
            #try to connect, return if unable to reach board
            if not self.connect():
                raise ValueError("Could not connect to board")

        # Loop to receive the complete data packet
        while len(data) < self.packet_size:
            packet_part = self.board.recv(self.packet_size - len(data))
            if not packet_part:
                raise ValueError("Connection closed by the server")
            data += packet_part

        for _ in SensorPackets:
            # Unpack the packet id
            packet_id = struct.unpack_from('<I', data, offset)[0]
            offset += 4

            # Unpack the float/int value
            if packet_id == SensorPackets.TIME.value:
                float_value = struct.unpack_from('<q', data, offset)[0]
            else:
                float_value = struct.unpack_from('<f', data, offset)[0]
            offset += 4

            sensor_data[SensorPackets(packet_id).value] = float_value
            
        return sensor_data
    
    def save_to_csv(self, path, filename):
        """Starts saving data from the board to a csv file with directory and file name. DO NOT INCLUDE .CSV

        Args:
            path (str): path to save file
            filename (str): file name to save under (don't include extension)
        """
        self.stopWriting = False
        with open(os.path.join(path, filename+".csv"), mode='w', newline='') as file:
            writer = csv.writer(file)
            
            #write header
            writer.writerow(self.list_values())
            
            while not self.stopWriting:
                writer.writerow(self.get_line())
                
    def list_values(self):
        columns = []
        for sensor in SensorPackets:
            columns.append(sensor.name)
        return columns

            
if __name__ == "__main__":
    file_name = "T1004_IMU2"
    save_file_path = os.path.join("data", "bmi270", "static", "Const")

    with open("config.json", "r") as file:
        config = json.load(file)

    board = wifiBoard("192.168.1.101", 80) #"192.168.1.101")
    
    board.connect()
    board.save_to_csv(save_file_path, file_name)