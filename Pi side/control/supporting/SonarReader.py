#SonarReader.py
#Polls all sonar sensors
#and constructs a string to send
#to the operator if any sonar states change.
import SonarTriggerEcho as sensor
import pigpio
import time
class Sonars:
    def __init__(self):
        RF_TRIG = 24
        RF_ECHO = 14
        LF_TRIG = 27
        LF_ECHO = 4
        RB_TRIG = 23
        RB_ECHO = 15
        LB_TRIG = 17
        LB_ECHO = 18
        TOGPIO = 10
        #list = [rf, lf, rb, lb]
        self.pi = pigpio.pi()
        self.pi.write(TOGPIO, 1)
        self.sensors = (sensor.ranger(self.pi, RF_TRIG, RF_ECHO),sensor.ranger(pigpio.pi(), LF_TRIG, LF_ECHO),sensor.ranger(pigpio.pi(), RB_TRIG, RB_ECHO),sensor.ranger(pigpio.pi(), LB_TRIG, LB_ECHO))
        #self.sensors = (sensor.ranger(self.pi, RF_TRIG, RF_ECHO),sensor.ranger(pigpio.pi(), LF_TRIG, LF_ECHO))
        self.CLOSE = -1
        self.OK = 0
        self.FAR = 1
        self.states = [self.FAR, self.FAR, self.FAR, self.FAR]
        self.distances = [0.0, 0.0, 0.0, 0.0]
    def readAll(self):
        msg = ""
        # .read() returns raw micros value. cm = micros/1000000.0*34030/2
        CLOSE = 30 #Less than CLOSE (in cm) = getting too close
        FAR = 100 #Greater than 100cm = too far for good reading
        ERROR_LOW = 6 #Sensors erroneously produce reads between ERROR_LOW and ERROR_HIGH
        ERROR_HIGH = 7
        for i in range(len(self.sensors)): #Read each sensor sequentially
            self.distances[i] = self.sensors[i].read()/1000000.0*34030/2
            #print(self.distances[i])
            if self.distances[i] > ERROR_LOW and self.distances[i] < ERROR_HIGH: continue #Bad reading
            elif self.distances[i] < CLOSE: #If this sensor reads too close
                if self.states[i] != self.CLOSE:
                    self.states[i] = self.CLOSE
                    msg += "{}c".format(i)
                    #Send "i is too close"
            elif self.distances[i] < FAR: #Between CLOSE and FAR
                if self.states[i] != self.OK:
                    self.states[i] = self.OK
                    msg += "{}o".format(i)
                    #Send "i is ok"
            else: #We're too far for consistent readings
                if self.states[i] != self.FAR:
                    self.states[i] = self.FAR
                    msg += "{}f".format(i)
                    #Send "i is too far"
        return msg
    def close(self):
        for i in range(len(self.sensors)): self.sensors[i].cancel()
        self.pi.stop()
