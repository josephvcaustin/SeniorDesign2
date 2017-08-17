from Server import Server
import RPi.GPIO as GPIO
import socket
import time
from time import sleep
TIMES_TO_TRY = 3
msglength = 7
greenLED = 9
redLED = 22
class Receiver:
    def __init__(self):
        #sleep(30) #Wait for wlan to connect on autostart
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(redLED, GPIO.OUT)
        GPIO.setup(greenLED, GPIO.OUT)
        #Client has not connected yet
        GPIO.output(redLED, GPIO.HIGH)
        GPIO.output(greenLED, GPIO.LOW)
        
        self.msglength = 7 #Character length of message is 7, longest message is LX-1000
        self.server = Server()
        self.retries = 0
        self.nextCheckTime = time.time() + 1.0
        #Client connected
        GPIO.output(redLED, GPIO.LOW)
        GPIO.output(greenLED, GPIO.HIGH) 

    def receive(self):
        msg = ""
        try: #Try to receive a message, except a timeout exception
            msg = self.server.c.recv(msglength)
            #If we don't time out waiting for a message, set retries to 0
            self.retries = 0
            if msg == "Q".ljust(msglength):
                self.server.sock.close()

            return msg #Return to main module to be decoded

        except (socket.timeout, socket.error): #Timed out receiving a message, do heartbeat
            #If the client doesn't respond after the first heartbeat, stop the motors.

            if(time.time() > self.nextCheckTime):
                if(self.retries > 0):
                    msg = "STOP" #Tell the decoder to stop everything
                self.server.c.send("<3") #ask the client if they're still there
                self.retries+=1 #Number of heartbeats sent to client without a response
                msg = "<3"
                self.nextCheckTime = time.time() + 1.0
                
                if(self.retries >= TIMES_TO_TRY): #They haven't responded to consecutive heartbeats, they lost connection
                    print "</3"
                    print "Loss of signal."
                    print "Waiting for client to reconnect..."
                    self.retries = 0
                    GPIO.output(greenLED, GPIO.LOW)
                    GPIO.output(redLED, GPIO.HIGH)
                    msg = "STOP!" #Stop the bot if an exception occurs
                    return msg
                    while True:
                        try:
                            GPIO.output(redLED, GPIO.LOW)
                            GPIO.output(greenLED, GPIO.HIGH)
                            msg = "STOP!"
                            return msg
                            sleep(5)
                            break
                        except Exception as inst:
                            print "No internet connection."
                            sleep(1)
                            continue 
                else: #Haven't exceeded retry limit, see if they have responded yet.
                    print "<3" #A heartbeat signal was sent
                    return msg #msg is empty or STOP
                    pass
            
        except Exception as inst: #Except any other exception, print out the exception to help with debugging.
            print "An unexpected error occurred in MessageReceiver.py:"
            print inst
            msg = "STOP!" #Stop the bot if an exception occurs
            return msg

    def send(self, msg): self.server.c.send(msg)

    def close(self):
        self.server.sock.close()
        self.server.sock = None
        self.server = None
        #Client will be disconnected
        GPIO.output(redLED, GPIO.HIGH)
        GPIO.output(greenLED, GPIO.LOW) 
