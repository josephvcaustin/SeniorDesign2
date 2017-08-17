#MessageDecoder.py
#Decodes 7-byte string commands
#and controlls motors, servos, and LEDs
from MotorController import MotorController
from ServoController import ServoController
from time import sleep
MOTOR_MODE = -1
SERVO_MODE = 0
ROUTINE_MODE = 1
PRECISION = 1000 #Encoded messages send values from -precision to precision read from analog controller input
msglength = 7
MIN_SERVO_SPEED = 10 #At least increment servo value by 10
MAX_SERVO_SPEED = 100 #At most increment servo value by 100
MAX_MOTOR_SPEED = 4000
STEER_DIRECTION = 1 #Negate this value if steering is backward.
class Decoder:
    def __init__(self):
        self.listening = True #Whether or not the bot should respond to a command
        self.stopped = False
        self.controllingServos = False #Whether or not to control servos this iteration
        self.controllingMotors = False #Whether or not to control motors this iteration
        self.sprint = False
        self.mode = MOTOR_MODE
        self.steeringRange = 2000
        self.motorRange = 2000
        self.servoSpeed = MIN_SERVO_SPEED
        self.steering = 0
        self.throttle = 0
        self.bot = 0
        self.mid = 0
        self.top = 0
        self.sc = ServoController()
        self.mc = MotorController()
        self.mc.stopMotors()
        self.sc.resetServos()
        sleep(0.5)
        self.sc.stopServos()
    #Snap all servos back to middle position.
    def resetServos(self):
        self.sc.resetServos()
        self.bot = 0
        self.mid = 0
        self.top = 0
    #Write STOP to the motors
    def stopMotors(self):
        self.mc.stopMotors()
        self.steering = 0
        self.throttle = 0
    #Write STOP to the servos (stop powering them)
    def stopServos(self):
        self.sc.stopServos()
        self.bot = 0
        self.mid = 0
        self.top = 0
############# MESSAGE DECODER ##############
    def decode(self, msg):
        msgToOperator = ""
        if not msg: return msgToOperator #If the string is empty, ignore
        #First assume we aren't going to control anything, change if we are
        self.controllingMotors = False
        self.controllingServos = False
        #B button will stop everything and stop listening, or resume listening
        if msg == "B".ljust(msglength):
            if self.listening: #If listening
                self.stopServos()
                self.stopMotors()
                self.listening = False
                msgToOperator = "NOT LISTENING"
            else: #If not listening
                self.listening = True
                msgToOperator = "LISTENING"
        elif msg == "STOP" or msg == "STOP!": #Stop all motors and servos
            self.stopMotors()
            self.stopServos()
            print "Forcing bot to stop."
            return
        #Back button quits
        elif msg == "Q".ljust(msglength):
            self.stopMotors()
            self.stopServos()
            self.mc.lightsOff()
            self.listening = False
            return
        elif not self.listening: return #If not listening, do nothing.
        #A button will turn on headlights
        elif msg == "A".ljust(msglength):
            if (self.mode == MOTOR_MODE):
                msgToOperator = "LIGHTS"
                self.mc.toggleHeadlights()
            elif(self.mode == ROUTINE_MODE):
                self.sc.reachArm()
        #X button will snap servos back to SERVO_MID
        elif msg == "X".ljust(msglength):
            msgToOperator = "SERVO RESET"
            self.resetServos()
        #Y button will power off servos
        elif msg == "Y".ljust(msglength):
            msgToOperator = "SERVO STOP"
            self.stopServos()
        #Start will change the mode of operation
        elif msg == "START".ljust(msglength):
            self.mode += 1
            if(self.mode > 1): self.mode = -1
            if(self.mode == MOTOR_MODE):
                msgToOperator = "DRIVE MODE"
                self.stopMotors()
                self.sc.rotateBase(0)
                self.sc.rotateEff(0)
            elif (self.mode == SERVO_MODE):
                msgToOperator = "MANIPULATOR MODE"
                self.stopMotors()
            else:
                msgToOperator = "ROUTINE MODE"
                self.stopMotors()
        #Rotate the base left or right, stop rotating when a bumper is released
        elif msg == "LP".ljust(msglength):
            if(self.mode == ROUTINE_MODE): self.sc.lowerForTunnel()
            else: self.sc.rotateBase(-1) #Rotate base left
        elif msg == "LR".ljust(msglength):
            self.sc.rotateBase(0) #Stop rotating
        elif msg == "RP".ljust(msglength):
            if(self.mode == ROUTINE_MODE): self.sc.raiseForDelivery()
            else: self.sc.rotateBase(1) #Rotate base right
        elif msg == "RR".ljust(msglength):
            self.sc.rotateBase(0) #Stop rotating
        #Left Stick X used for steering
        elif msg[:2] == "LX":
            lxVal = int(msg[2:]) #Left stick X val from -1000 to 1000
            if (self.mode == MOTOR_MODE):
                self.steering = STEER_DIRECTION * int(float(lxVal)/PRECISION * self.steeringRange)
                self.controllingMotors=True
        #Left Stick Y used to control the middle servo
        elif msg[:2] == "LY":
            val = int(msg[2:]) #Left stick Y val from -1000 to 1000
            if (self.mode == SERVO_MODE):
                self.controllingServos=True
                valPercent = float(val)/float(PRECISION)
                self.mid = int(valPercent * self.servoSpeed)*(-1)
        elif msg[:2] == "RX":
            val = int(msg[2:]) #Right stick X val from -1000 to 1000
        #Right Stick Y Value used to control the top servo
        elif msg[:2] == "RY":
            val = int(msg[2:]) #Left stick Y val from -1000 to 1000
            if (self.mode != ROUTINE_MODE):
                self.controllingServos=True
                valPercent = float(val)/float(PRECISION)
                self.top = int(valPercent * self.servoSpeed)
        #Right Trigger used to control throttle and the bottom servo
        elif msg[:2] == "RT":
            #Multiply val by -1 to flip trigger direction
            val = int(msg[2:]) #trigger val from 0 to 1000
            if (self.mode == MOTOR_MODE):
                self.throttle = int(float(val)/float(PRECISION) * float(self.motorRange)) #From -motorRange to motorRange 
                self.controllingMotors=True
            elif (self.mode == SERVO_MODE):
                self.controllingServos=True
                valPercent = float(val)/float(PRECISION)
                self.bot = int(valPercent * self.servoSpeed)*(-1)
        #DPAD X used to increase/decrease steering speed or servo movement speed
        elif msg[:2] == "DX":
            val = int(msg[2:]) #Dpad X val (-1 = left, 0 = center, 1 = right)
            if (self.mode == MOTOR_MODE):
                self.steeringRange += 100*val #Increment or decrement the steering speed
                if self.steeringRange > MAX_MOTOR_SPEED: self.steeringRange = MAX_MOTOR_SPEED
                elif self.steeringRange < 0: self.steeringRange = 0
                msgToOperator = "Steer: {}".format(self.steeringRange)
            elif (self.mode == SERVO_MODE):
                self.servoSpeed += 10*val #increment or decrement the servo speed by 10
                if self.servoSpeed < MIN_SERVO_SPEED: self.servoSpeed = MIN_SERVO_SPEED
                elif self.servoSpeed > MAX_SERVO_SPEED: self.servoSpeed = MAX_SERVO_SPEED
                msgToOperator = "Servo: {}".format(self.servoSpeed)
            else:
                if(val > 0):
                    self.steeringRange = 500
                    self.motorRange = 4000
                    msgToOperator = "SPRINT"
                    self.sprint = True
                elif(val < 0):
                    self.steeringRange = 2000
                    self.motorRange = 2000
                    msgToOperator = "NORMAL"
                    self.sprint = False
        #DPAD Y used to increase/decrease max throttle or to extend/retract the effector
        elif msg[:2] == "DY":
            val = int(msg[2:]) #Dpad Y val (-1 = down, 0 = center, 1 = up)
            if (self.mode == MOTOR_MODE):
                self.motorRange += 100*val #Increment or decrement the max speed
                if self.motorRange > MAX_MOTOR_SPEED: self.motorRange = MAX_MOTOR_SPEED
                elif self.motorRange < 0: self.motorRange = 0
                msgToOperator = "Throttle: {}".format(self.motorRange)
            elif (self.mode == SERVO_MODE): self.sc.rotateEff(val)
            else:
                if(self.sprint):
                    if val < 0: self.mc.trimVal -= 10
                    elif val > 0: self.mc.trimVal += 10
                    msgToOperator = "Trim {}".format(self.mc.trimVal)
                else:
                    if (val < 0): self.sc.retractEff()
                    elif (val > 0): self.sc.extendEff()
        #If need to update throttle/steering on motors, tell motorcontroller to update it
        if (self.controllingMotors): self.mc.controlMotors(self.steering, self.throttle)
        #If need to update servo positions, tell servocontroller to update them
        if (self.controllingServos): self.sc.controlServos(self.bot, self.mid, self.top)
        return msgToOperator
    def close(self):
       self.stopMotors()
       self.stopServos()
       self.mc = None
       self.sc = None
