import serial
import json
from time import time
import os

file_name = "v1_tempchange"
save_file_path = os.path.join("data", "bmi270", "static", file_name+".bin")

with (open("config.json", "r")) as file:
    config = json.load(file)
    
board = serial.Serial(config["port"], config["baud"])
board.write(b'\n') #start process
lines  = 0
startTime = time()
with open(save_file_path, 'wb') as f:
    try: 
        while True:
            line = board.readline()
            if not line:
                break
            f.write(line)
            
            # Print a line every second
            lines += 1
            now= time()
            if  (now - startTime) >= 1:
                print(line) 
                lines = 0
                startTime = now # roughly 150hz
            
    except Exception as e:
        print(e)
        board.flush()
        board.close()
