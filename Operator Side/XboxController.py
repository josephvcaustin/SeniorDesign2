#XboxController.py
#Xbox Controller object used for reading input from
#a Microsoft Xbox 360 controller. Saves values read
#from controller to variables.
import sys, pygame
from time import sleep
from SonarGUI import SonarGUI
###Button Constants###
A_BUTTON = 0
B_BUTTON = 1
X_BUTTON = 2
Y_BUTTON = 3
LBUMPER = 4
RBUMPER = 5
BACK = 6
START = 7
GUIDE = 8
#######################
###Trigger Constants###
LEFTSTICK_X = 0
LEFTSTICK_Y = 1
RIGHTSTICK_X = 4
RIGHTSTICK_Y = 3
TRIGGER = 2
DEADZONE = 0.2 #Ignore analog values from sticks less
                #than 0.2 on either side for better control.
                #A reading of 0 indicated perfectly centered.
class XboxController:
    def __init__(self):
        ###Draw the frame on the screen###
        pygame.init()
        size = 520, 520
        self.screen = pygame.display.set_mode(size)
        pygame.event.set_allowed(pygame.QUIT) #Make event polling faster by only checking for quit
        ###################################
        self.xbox = None
        pygame.joystick.init()
        try:
            self.xbox = pygame.joystick.Joystick(0) #assume only Xbox controller is plugged in
            self.xbox.init() #start the joystick
        except:
            print "No Xbox controller is connected."
            pygame.display.quit()
            sys.exit()
        ###Current Values###
        self.lsx_val = 0 #Left Stick X
        self.lsy_val = 0 #Left Stick Y
        self.rsx_val = 0 #Right Stick X
        self.rsy_val = 0 #Right Stick Y
        self.trigger_val = 0 #Right and left triggers
        self.A = False
        self.B = False
        self.X = False
        self.Y = False
        self.LB = False
        self.RB = False
        self.BACK = False
        self.START = False
        self.GUIDE = False #Exclusively for quitting robot operation entirely
        self.dpad_x = 0
        self.dpad_y = 0
        self.quitting = False #Used for closing the frame
    #Call to read all controller input values
    #Should be called in a loop to poll for controller input
    #Loop must check if the quitting variable is set to create a breakpoint
    def getInput(self):
        self.quitting = False
        event = pygame.event.poll() #Read all values on the controller
        if event.type == pygame.QUIT: #Used for closing the frame cleanly.
            self.quitting = True
        if(abs(self.xbox.get_axis(LEFTSTICK_X)) > DEADZONE):
            self.lsx_val = self.xbox.get_axis(LEFTSTICK_X)
        else: self.lsx_val = 0
        if(abs(self.xbox.get_axis(LEFTSTICK_Y)) > DEADZONE):
            self.lsy_val = self.xbox.get_axis(LEFTSTICK_Y)
        else: self.lsy_val = 0
        if(abs(self.xbox.get_axis(RIGHTSTICK_X)) > DEADZONE):
            self.rsx_val = self.xbox.get_axis(RIGHTSTICK_X)
        else: self.rsx_val = 0
        if(abs(self.xbox.get_axis(RIGHTSTICK_Y)) > DEADZONE):
            self.rsy_val = self.xbox.get_axis(RIGHTSTICK_Y)
        else: self.rsy_val = 0
        self.trigger_val = self.xbox.get_axis(TRIGGER) #Z axis value, -1 if RT fully pressed, 1 if LT fully pressed
        self.dpad_x, self.dpad_y = self.xbox.get_hat(0) #Returns an (x, y) tuple
        if(self.xbox.get_button(A_BUTTON)):
            #print "A"
            self.A = True
        else: self.A = False
        if(self.xbox.get_button(B_BUTTON)):
            #print "B"
            self.B = True
        else: self.B = False
        if(self.xbox.get_button(X_BUTTON)):
            #print "X"
            self.X = True
        else: self.X = False
        if(self.xbox.get_button(Y_BUTTON)):
            #print "Y"
            self.Y = True
        else: self.Y = False
        if(self.xbox.get_button(LBUMPER)):
            #print "LB"
            self.LB = True
        else: self.LB = False
        if(self.xbox.get_button(RBUMPER)):
            #print "RB"
            self.RB = True
        else: self.RB = False
        if(self.xbox.get_button(BACK)):
            #print "BACK"
            self.BACK = True
            self.quitting = True
        else: self.BACK = False
        if(self.xbox.get_button(START)):
            #print "START"
            self.START = True
        else: self.START = False
        if(self.xbox.get_button(GUIDE)):
            #print "GUIDE"
            self.GUIDE = True
            self.quitting = True
        if self.quitting:
            print "Quitting."
            pygame.display.quit()
