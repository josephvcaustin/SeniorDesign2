# RunThis.py
# Top level module on the Raspberry Pi for operating the robot
# Instantiates other supporting modules for robot operation:
# MessageReceiver, MessageDecoder, and SonarReader.
import sys
from time import sleep
import time
sys.path.append("/home/pi/Desktop/SeniorDesign2/Control/Supporting")
sys.path.append("/home/pi/Desktop/SeniorDesign2/Control/Adafruit")
from MessageReceiver import Receiver
r = Receiver()
from MessageDecoder import Decoder
d = Decoder()
from SonarReader import Sonars
s = Sonars()
msglength = 7
while True:
    try:
        #RECEIVE
        msg = r.receive() #Heartbeat after 1 second of not
                          #receiving anything 
        #DECODE, EXECUTE
        #Send a message to operator if there is one
        msgToOperator = d.decode(msg)
        if msg == "STOP!": #An exception occurred
            print "Rebooting Bot."
            r.close()
            r = None
            d.close()
            d = None
            s.close()
            s = None
            sleep(3)
            r = Receiver()
            d = Decoder()
            s = Sonars()
            continue
        elif msg == "Q".ljust(msglength):
            print "Quitting."
            r.close()
            r = None
            d.close()
            d = None
            s.close()
            s = None
            sleep(3)
            r = Receiver()
            d = Decoder()
            s = Sonars()
            continue
        else:
            #Send message from decoder
            if msgToOperator:
                r.send(msgToOperator)

            #Send message from sonars
            msgToOperator = s.readAll()
            if msgToOperator:
                r.send(msgToOperator)               
    except Exception as inst:
        print inst
        print "Error, Rebooting Bot."
        sleep(1)
        r.close()
        r = None
        d.close()
        d = None
        s.close()
        s = None
        sleep(3)
        r = Receiver()
        d = Decoder()
        s = Sonars()
        continue
