import sonar_trigger_echo as sensor
import pigpio
import curses
import time
import sys
import os

#os.system("sudo pigpiod")

#create sensor objecs
sensors = (sensor.ranger(pigpio.pi(), 19, 16), sensor.ranger(pigpio.pi(),13, 12))
scr = curses.initscr()
scr.addstr(0, 0, "Right = ")
scr.addstr(1, 0, "Left = ")

CLOSE = 15
FAR = 100
L_ERROR_HIGH = 7
L_ERROR_LOW = 6

while True:

    # .read() returns raw micros value. cm = micros/1000000.0*34030/2
    rDist = sensors[0].read()/1000000.0*34030/2
    lDist = sensors[1].read()/1000000.0*34030/2
    scr.addstr(0,10,str(rDist))
    scr.addstr(1,10,str(lDist))
    scr.refresh()
    #print "Right: {:0.4f} || Left: {}".format(rDist,lDist)
    if rDist < CLOSE:
        scr.addstr(0,25,"Close!")
    elif rDist < FAR and rDist >= CLOSE:
        scr.addstr(0,25,"OK!   ")
    else:
        scr.addstr(0,25,"?     ")
    if (lDist < 10 and lDist >L_ERROR_HIGH) or (lDist < L_ERROR_LOW):
        scr.addstr(1,25,"Close!")
    elif lDist < FAR and lDist >= CLOSE:
        scr.addstr(1,25,"OK!   ")
    else:
        scr.addstr(1,25,"?     ")

