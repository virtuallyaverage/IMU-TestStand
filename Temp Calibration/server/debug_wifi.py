import json
import socket
import struct
from time import time
  


def receive_data(ip, port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        while True:
            data = s.recv(4)  # 4 bytes for a float
            if not data:
                break
            temp = struct.unpack('f', data)[0]
            print("Received:", temp)

if __name__ == "__main__":
    
    with (open("config.json", "r")) as file:
        config = json.load(file)
    
    receive_data(config["ip"], config["wifi_port"])