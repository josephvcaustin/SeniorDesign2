#!/usr/bin/python

from Adafruit_PWM_Servo_Driver_PIGPIO import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 307  # Min pulse length out of 4096
servoMax = 922  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 100                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(100)                        # Set frequency to 60 Hz
while (True):
  # Change speed of continuous servo on channel O
    pwm.setPWM(11, 0, servoMin+610)
    time.sleep(2)
    pwm.setPWM(11, 0, servoMin)
    time.sleep(2)



