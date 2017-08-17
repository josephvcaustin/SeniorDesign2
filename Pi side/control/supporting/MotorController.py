#MotorController.py
#Receives arguments from MessageDecoder.py
#and exerts control over the motors and LEDs.
from Adafruit_PWM_Servo_Driver_PIGPIO import PWM
import RPi.GPIO as GPIO
import warnings
warnings.filterwarnings("ignore") #Ignore GPIO warnings
### Motor Pins ###
LEFT_MOTOR_CHANNEL = 6
RIGHT_MOTOR_CHANNEL = 7
LEFT_DIRECTION_PIN = 20
RIGHT_DIRECTION_PIN = 26
##################
HEADLIGHTS = 19
### Booleans to indicate motor direction ###
RIGHT_MOTOR_FORWARD = False #Change to True if motors are backward
RIGHT_MOTOR_BACKWARD = not RIGHT_MOTOR_FORWARD #Opposite of forward
LEFT_MOTOR_FORWARD = RIGHT_MOTOR_FORWARD #Opposite of right
LEFT_MOTOR_BACKWARD = RIGHT_MOTOR_BACKWARD
############################################
MAX_SPEED = 4090 #Max Speed
STOP = 4096
THRESHOLD = 300 #Speed threshold for considering to be stopped to prevent buzzing.
FREQ = 100 #Motor PWM frequency
HAT_ADDR = 0x40 #Pi hat address
class MotorController:
    def __init__(self):
        self.pwm = PWM(HAT_ADDR)
        self.pwm.setPWMFreq(FREQ)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RIGHT_DIRECTION_PIN, GPIO.OUT)
        GPIO.setup(LEFT_DIRECTION_PIN, GPIO.OUT)
        GPIO.setup(HEADLIGHTS, GPIO.OUT)
        GPIO.output(RIGHT_DIRECTION_PIN, RIGHT_MOTOR_FORWARD)
        GPIO.output(LEFT_DIRECTION_PIN, LEFT_MOTOR_FORWARD)
        GPIO.output(HEADLIGHTS, GPIO.LOW)
        self.pwm.setPWM(RIGHT_MOTOR_CHANNEL, 0, STOP)
        self.pwm.setPWM(LEFT_MOTOR_CHANNEL, 0, STOP)
        self.lightsOn = False
        self.trimVal = 150
    def controlMotors(self, steering, throttle):
        #################### Calculate motor values ########################
        #Motors will turn the bot based on the LX steering value plus
        #the value of throttle to allow both turning in place and
        #turning while going forward/back.
        newRightVal = 0
        newLeftVal = 0
        if (steering == 0): #Both motors going straight
            newRightVal = throttle
            newLeftVal = throttle
        else:
            newRightVal = (((-1)*steering) + throttle) #Right motor speed is always opposite of steering input
            newLeftVal = steering+throttle
        #Write "stop" to prevent motors buzzing at low speeds.
        if abs(newRightVal) < THRESHOLD: newRightVal = STOP
        elif(newRightVal < 0): #Right motors are running backward.
            GPIO.output(RIGHT_DIRECTION_PIN, RIGHT_MOTOR_BACKWARD)
            newRightVal*=-1 #newRightVal is negative, so make it positive before asserting.
        else: GPIO.output(RIGHT_DIRECTION_PIN, RIGHT_MOTOR_FORWARD)
        #Write "stop" to prevent motors buzzing at low speeds.
        if abs(newLeftVal) < THRESHOLD: newLeftVal = STOP
        elif(newLeftVal < 0): #Left motors are running backward.
            GPIO.output(LEFT_DIRECTION_PIN, LEFT_MOTOR_BACKWARD)
            newLeftVal*=-1 #newLeftVal is negative, so make it positive before asserting.
        else: GPIO.output(LEFT_DIRECTION_PIN, LEFT_MOTOR_FORWARD)
        ####################################################################
        if newRightVal != STOP: newRightVal -= self.trimVal
        if newRightVal < THRESHOLD: newRightVal = STOP
        #Assert control on right and left motors
        self.pwm.setPWM(RIGHT_MOTOR_CHANNEL, 0, newRightVal)
        self.pwm.setPWM(LEFT_MOTOR_CHANNEL, 0, newLeftVal)
        #print "Right = {}".format(newRightVal)
        #print "Left = {}".format(newLeftVal)
    def stopMotors(self):
        self.controlMotors(0, STOP)
    def lightsOff(self):
        GPIO.output(HEADLIGHTS, GPIO.LOW)
    def toggleHeadlights(self):
        self.lightsOn = not self.lightsOn
        if self.lightsOn: GPIO.output(HEADLIGHTS, GPIO.HIGH)
        else: GPIO.output(HEADLIGHTS, GPIO.LOW)
