#RunThis.py
#Top level module on operator's machine for driving
#the robot over the internet. Sends 7-byte string
#commands to robot to be decoded and executed.
#Renders Sonar data to operator using a GUI.
import sys
from time import sleep
from XboxController import XboxController
from Client import Client
import socket
from SonarGUI import SonarGUI
controller = XboxController()
gui = SonarGUI(controller.screen)
sleep(0.5) #Delay between setting up controller and communicating with bot
client = Client()
connected = True
client.sock.setblocking(0) #Non-blocking, time out immediately if buffer is empty
msglength = 7 #character length of each instruction string
              #length of 7 based on maxval being 1000, longest instruction
              #is LX-1000 (7 characters)
#Values used to only send if they change
lsx_prev = 0 #Left Stick X
lsy_prev = 0 #Left Stick Y
rsx_prev = 0 #Right Stick X
rsy_prev = 0 #Right Stick Y
trigger_prev = 0 #Right Trigger and left triggers
dpad_x_prev = 0
dpad_y_prev = 0
A_prev = False
B_prev = False
X_prev = False
Y_prev = False
LB_prev = False
RB_prev = False
BACK_prev = False
START_prev = False
GUIDE_prev = False
polltime = 0.1 #Time between controller input reads and packet sending
maxval = 1000 #Encode stick and trigger input as values from -max to max
retries = 0
TIMES_TO_TRY = 30 #Times to check if something is in the buffer before determining LOS
#Sonar Constants
OK = 0
CLOSE = 1
FAR = 2
#Poll input, encode, and send
while True:
    #Only send 4 messages per poll
    buttonMsg = ""
    stickMsgX = ""
    stickMsgY = ""
    triggerMsg = ""
    sleep(polltime) #Sleep to prevent flooding the buffer with commands
    controller.getInput() #read all values from controller
    if controller.quitting: #Quitting handled by XboxController object
        client.send("Q".ljust(msglength))
        client.sock.close()
        sys.exit()
    #If the operator's side boots and can't connect,
    #Try again until connection is established.
    if not connected:
        if not client.reconnect(): continue
        else: connected = True 
    #Only send "A", "B", "X", "Y", "BACK", or "START"
    #one time when the button is pressed down.
    #Suppress multiple button input (not needed)
    if (A_prev == False) and (controller.A == True):
        A_prev = True
        buttonMsg ="A".ljust(msglength)
    elif (controller.A == False):
        A_prev = False
    if (B_prev == False) and (controller.B == True):
        B_prev = True
        buttonMsg = "B".ljust(msglength)
    elif (controller.B == False):
        B_prev = False
    if (X_prev == False) and (controller.X == True):
        X_prev = True
        buttonMsg = "X".ljust(msglength)
    elif (controller.X == False):
        X_prev = False
    if (Y_prev == False) and (controller.Y == True):
        Y_prev = True
        buttonMsg = "Y".ljust(msglength)
    elif (controller.Y == False):
        Y_prev = False
    if (BACK_prev == False) and (controller.BACK == True):
        BACK_prev = True
        buttonMsg = "BACK".ljust(msglength)
    elif (controller.BACK == False):
        BACK_prev = False
    if (START_prev == False) and (controller.START == True):
        START_prev = True
        buttonMsg = "START".ljust(msglength)
    elif (controller.START == False):
        START_prev = False
    #Send "LP" when LB is pressed, send "LR" when it is released.
    #Used to indicate the bumper is being held.
    if (LB_prev == False) and (controller.LB == True):
        LB_prev = True
        buttonMsg = "LP".ljust(msglength)
    elif (LB_prev == True) and (controller.LB == False):
        LB_prev = False
        buttonMsg = "LR".ljust(msglength)

    #Send "RP" when RB is pressed, send "RR" when it is released.
    #Used to indicate the bumper is being held.
    if (RB_prev == False) and (controller.RB == True):
        RB_prev = True
        buttonMsg = "RP".ljust(msglength)
    elif (RB_prev == True) and (controller.RB == False):
        RB_prev = False
        buttonMsg = "RR".ljust(msglength)
    if (lsx_prev != controller.lsx_val):
        lsx_prev = controller.lsx_val
        val = int(maxval*controller.lsx_val)
        stickMsgX = "LX{}".format(val).ljust(msglength)
    if (lsy_prev != controller.lsy_val):
        lsy_prev = controller.lsy_val
        val = int(maxval*controller.lsy_val)
        stickMsgY = "LY{}".format(val).ljust(msglength)
    if (rsx_prev != controller.rsx_val):
        rsx_prev = controller.rsx_val
        val = int(maxval*controller.rsx_val)
        stickMsgX = "RX{}".format(val).ljust(msglength)
    if (rsy_prev != controller.rsy_val):
        rsy_prev = controller.rsy_val
        val = int(maxval*controller.rsy_val)
        stickMsgY = "RY{}".format(val).ljust(msglength)
    if (trigger_prev != controller.trigger_val):
        trigger_prev = controller.trigger_val
        val = int(maxval*controller.trigger_val)
        triggerMsg = "RT{}".format(val).ljust(msglength)
    if (dpad_x_prev != controller.dpad_x):
        dpad_x_prev = controller.dpad_x
        buttonMsg = "DX{}".format(dpad_x_prev).ljust(msglength)
    if (dpad_y_prev != controller.dpad_y):
        dpad_y_prev = controller.dpad_y
        buttonMsg = "DY{}".format(dpad_y_prev).ljust(msglength)
    #Only send one type of each message at a time
    if buttonMsg: client.send(buttonMsg)
    if triggerMsg: client.send(triggerMsg)
    if stickMsgX: client.send(stickMsgX)
    if stickMsgY: client.send(stickMsgY)
    #Check and see if there's anything in the buffer.
    try:
        msg = client.sock.recv(1024)
        #Bot probably sent back some sonar info
        sonars = [-1, -1, -1, -1]
        for i in range(len(sonars)):
            if "%sc"%(i) in msg:
                sonars[i] = CLOSE
                strn = "{}c".format(i)
                msg = msg.replace(strn, "")
            if "%so"%(i) in msg:
                sonars[i] = OK
                strn = "{}o".format(i)
                msg = msg.replace(strn, "")
            if "%sf"%(i) in msg:
                sonars[i] = FAR
                strn = "{}f".format(i)
                msg = msg.replace(strn, "")
        gui.updateSonars(sonars)
        if msg: print msg
        client.send("h".ljust(msglength)) #Tell server "I heard you"
        retries = 0
    except socket.timeout as inst: #Except the timeout exception if buffer is empty.
        print retries
        retries+=1
        if(retries > TIMES_TO_TRY):
                retries = 0
                print "Lost connection to server."
                connected = False 
        continue
    except Exception as inst:
        #[Errno 10035] A non-blocking socket operation could not be completed immediately
        #Will usually occur from trying to read from the pipe
        continue
