import os
import math

preamble = f"""
; accelPreamble    
M107
;TYPE:Custom
; Initial setups
G90 ; use absolute coordinates
G21 ; set units to millimeters

; Home
G1 Z50 F3000 ; move z up 2inches
G28 ; home all axes

; Set Feedrates
M203 Y$ ; set max feedrate mm/s


"""
def acellPreamble(max_feed: int) -> str: 
    return preamble.replace("$", f"{max_feed: 0.3f}")

def setAccell(Gs: int) -> str:
    return f"M204 T{9810*Gs: .3f} ; set travel accel to {Gs} G's\n"

cycle_y = """
G1 Y{max_y: .3f} ; cycle bed
G1 Y{min_y: .3f}
M400 ; wait for complete
"""

def cycleY(min_y, max_y) -> str:
    return cycle_y.format(max_y = max_y, min_y = min_y)

def gToMM(G: float) -> float:
    return G * 9810

def distToMaxFeed(accelMM: float, max_feed) -> float:
    initial_velocity = 0
    return (max_feed**2 - initial_velocity**2) / (2 * accelMM)

if __name__ == "__main__":
    MAX_Y = 270 #mm
    MIN_Y = 30 #mm
    MIN_TRAVEL = 10 #mm
    Y_DIST = MAX_Y-MIN_Y
    
    MAX_FEED = 200 # mm/s
    
    accel_list = [0.1, 0.2, 0.3]
    loopsPerAccel = 5
    
    gcode_name = "AccelTest.gcode"
    with open(gcode_name, 'w') as file:
        file.write(acellPreamble(MAX_FEED))
        
        for accel in accel_list:
            needed_feedrate = math.sqrt(2 * gToMM(accel) * Y_DIST)
            if needed_feedrate > MAX_FEED:
                print(f"{needed_feedrate: .1f}mm/s Needed for {accel}G's. Only {MAX_FEED} allowed.")
                min_y = MIN_Y
                max_y = MIN_Y+distToMaxFeed(gToMM(accel), MAX_FEED)
                if (max_y -min_y) >= MIN_TRAVEL:
                    print(f"Setting to {max_y - min_y}mm travel distance ")
                else:
                    print(f"Travel: {max_y-min_y}mm to low. Ending")
                    break
            
            file.write(setAccell(accel))
            for _ in range(loopsPerAccel):
                file.write(cycleY(min_y, max_y))
                
    print("done")
        
        
        
        
    

