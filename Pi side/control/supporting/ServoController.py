#ServoController.py
#Receives arguments from MessageDecoder.py
#and exerts control over the servos. Also runs
#programmed routines on manipulator arm.
from Adafruit_PWM_Servo_Driver_PIGPIO import PWM
from time import sleep
#Max and min assertable PWM values given freq=100
#SERVO_MIN = 307
#SERVO_MID_VAL = 635
#SERVO_MAX = 921
SERVO_MIN = 250
SERVO_MID_VAL = 635
SERVO_MAX = 1050
#Servo pin values
SERVO_EFF = 0
SERVO_TOP = 1
SERVO_MID = 2
SERVO_BOT = 3
SERVO_BASE = 4
STOP = 4096
FREQ = 100 #PWM freq
HAT_ADDR = 0x40 #Pi hat address
class ServoController:
    def __init__(self):
        self.servoTopVal = STOP #Value to assert on servo
        self.servoBotVal = STOP
        self.servoMidVal = STOP
        self.pwm = PWM(HAT_ADDR)
        self.pwm.setPWMFreq(FREQ)
        #setPWM(pin, channel, value)
        self.pwm.setPWM(SERVO_BOT, 0, self.servoBotVal)
        self.pwm.setPWM(SERVO_MID, 0, self.servoMidVal)
        self.pwm.setPWM(SERVO_TOP, 0, self.servoTopVal)
    #Write a specific value to all the servos
    def setServos(self, bot, mid, top):
        self.servoBotVal = bot
        self.servoMidVal = mid
        self.servoTopVal = top
        if(self.servoBotVal > SERVO_MAX) and not (self.servoBotVal == STOP): self.servoBotVal = SERVO_MAX
        elif(self.servoBotVal < SERVO_MIN): servoBotVal = SERVO_MIN
        if(self.servoMidVal > SERVO_MAX) and not (self.servoMidVal == STOP): self.servoMidVal = SERVO_MAX
        elif(self.servoMidVal < SERVO_MIN): self.servoMidVal = SERVO_MIN
        if(self.servoTopVal > SERVO_MAX) and not (self.servoTopVal == STOP): self.servoTopVal = SERVO_MAX
        elif(self.servoTopVal < SERVO_MIN): self.servoTopVal = SERVO_MIN
        self.pwm.setPWM(SERVO_BOT, 0, self.servoBotVal)
        self.pwm.setPWM(SERVO_MID, 0, self.servoMidVal)
        self.pwm.setPWM(SERVO_TOP, 0, self.servoTopVal)
    #Assert a new value on the servos by adding the value passed in to the existing PWM value
    def controlServos(self, bot, mid, top):
        self.servoBotVal += bot
        self.servoMidVal += mid
        self.servoTopVal += top
        if(self.servoBotVal > SERVO_MAX) and not (self.servoBotVal == STOP): self.servoBotVal = SERVO_MAX
        elif(self.servoBotVal < SERVO_MIN): servoBotVal = SERVO_MIN
        if(self.servoMidVal > SERVO_MAX) and not (self.servoMidVal == STOP): self.servoMidVal = SERVO_MAX
        elif(self.servoMidVal < SERVO_MIN): self.servoMidVal = SERVO_MIN
        if(self.servoTopVal > SERVO_MAX) and not (self.servoTopVal == STOP): self.servoTopVal = SERVO_MAX
        elif(self.servoTopVal < SERVO_MIN): self.servoTopVal = SERVO_MIN
        self.pwm.setPWM(SERVO_BOT, 0, self.servoBotVal)
        self.pwm.setPWM(SERVO_MID, 0, self.servoMidVal)
        self.pwm.setPWM(SERVO_TOP, 0, self.servoTopVal)
    def rotateBase(self, direction):
        #-1 = CCW, 0 = Stop, 1 = CW
        #Use a fixed speed that isn't the max speed
        if(direction < 0): self.pwm.setPWM(SERVO_BASE, 0, SERVO_MIN+300)
        elif(direction > 0): self.pwm.setPWM(SERVO_BASE, 0, SERVO_MAX-300)
        else: self.pwm.setPWM(SERVO_BASE, 0, STOP)
    def rotateEff(self, direction):
        #-1 = Retract, 0 = Stop, 1 = Extend
        #Just use the max speed
        if(direction < 0): self.pwm.setPWM(SERVO_EFF, 0, SERVO_MIN)
        elif(direction > 0): self.pwm.setPWM(SERVO_EFF, 0, SERVO_MAX)
        else: self.pwm.setPWM(SERVO_EFF, 0, STOP)
    def resetServos(self):
        self.setServos(679, 698, 722)
        self.rotateBase(0)
        self.rotateEff(0)
    def stopServos(self):
        self.setServos(STOP, STOP, STOP)
        self.servoBotVal = SERVO_MID_VAL
        self.servoMidVal = SERVO_MID_VAL
        self.servoTopVal = SERVO_MID_VAL
        self.rotateBase(0)
        self.rotateEff(0)
    def reachArm(self):
        self.resetServos()
        while(self.servoBotVal < 800):
            self.controlServos(20, 0, 0)
            sleep(0.1)
        while(self.servoTopVal < 840):
            self.controlServos(0, 0, 20)
            sleep(0.1)
        while(self.servoBotVal < 970):
            self.controlServos(20, 0, 0)
            sleep(0.1)
        while(self.servoMidVal < 550):
            self.controlServos(0,20,0)
            sleep(0.1)
    def raiseForDelivery(self):
        self.resetServos()
        sleep(0.1)
        while(self.servoMidVal < 1050):
            self.controlServos(0, 30, 0)
            sleep(0.1)
        while(self.servoTopVal < 870):
            self.controlServos(0, 0, 30)
            sleep(0.1)
    def lowerForTunnel(self):
        self.resetServos()
        sleep(0.1)
        while(self.servoMidVal < 920):
            self.controlServos(0, 10, 0)
            sleep(0.1)
        while(self.servoBotVal > 450):
            self.controlServos(-10, 0, 0)
            sleep(0.1)
        while(self.servoBotVal < 500):
            self.controlServos(10, 0, 0)
            sleep(0.1)
    def retractEff(self):
        self.rotateEff(-1)
        sleep(5.2)
        self.rotateEff(0)
    def extendEff(self):
        self.rotateEff(1)
        sleep(5.0)
        self.rotateEff(0)
            
