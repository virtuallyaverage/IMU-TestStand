
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
M203 Y 200.000 ; set max feedrate mm/s


M204 T 981.000 ; set travel accel to 0.1 G's

G1 Y 50.387 ; cycle bed
G1 Y 30.000
M400 ; wait for complete

G1 Y 50.387 ; cycle bed
G1 Y 30.000
M400 ; wait for complete

G1 Y 50.387 ; cycle bed
G1 Y 30.000
M400 ; wait for complete

G1 Y 50.387 ; cycle bed
G1 Y 30.000
M400 ; wait for complete

G1 Y 50.387 ; cycle bed
G1 Y 30.000
M400 ; wait for complete
M204 T 1962.000 ; set travel accel to 0.2 G's

G1 Y 40.194 ; cycle bed
G1 Y 30.000
M400 ; wait for complete

G1 Y 40.194 ; cycle bed
G1 Y 30.000
M400 ; wait for complete

G1 Y 40.194 ; cycle bed
G1 Y 30.000
M400 ; wait for complete

G1 Y 40.194 ; cycle bed
G1 Y 30.000
M400 ; wait for complete

G1 Y 40.194 ; cycle bed
G1 Y 30.000
M400 ; wait for complete
M400 ; wait to finish