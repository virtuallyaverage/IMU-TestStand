import json
import serial
from time import time

with (open("config.json", "r")) as file:
    config = json.load(file)
    
board = serial.Serial(config["port"], config["baud"]);
board.write(b'\n') #start process

startTime = time()
lines = 0
while True:
    value = board.readline()
    lines += 1
    now= time()
    if  (now - startTime) >= 1:
        print(value)
        print(lines/(now-startTime))
        lines = 0
        startTime = now # roughly 150hz
    
    
    