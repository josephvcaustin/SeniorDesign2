#SonarGUI.py
#Draws a GUI to the screen with
#symbols to indicate sonar readings.
import sys, pygame
from time import sleep
class SonarGUI:
    def __init__(self, scr):
        
        ###Draw the frame on the screen###
        self.screen = scr
        self.GREY = 50, 50, 50
        self.screen.fill(self.GREY)
        pygame.display.set_caption('Robot Control Interface')
        botImg = pygame.image.load("bot.png")
        self.warnImg = pygame.image.load("warning.png")
        self.okImg = pygame.image.load("ok.png")
        self.qImg = pygame.image.load("q.png")
        pygame.display.flip()
        #0  1  2  3
        #RF LF RB LB
        self.imgPositions = [(384, 0), (0, 0), (384, 384), (0, 384)]
        self.screen.blit(botImg, (107, 107))
        pygame.event.set_allowed(pygame.QUIT)
        pygame.mixer.music.load("buzzer.mp3")
        ###################################
        self.OK = 0
        self.CLOSE = 1
        self.FAR = 2
        self.sonars = [self.FAR, self.FAR, self.FAR, self.FAR]
        for i in range(len(self.sonars)):
            self.screen.blit(self.qImg, self.imgPositions[i])
        pygame.display.flip()
    def updateSonars(self, readings):
        pygame.mixer.music.rewind()
        for i in range(len(self.sonars)):
            if self.sonars[i] != readings[i]: #Only update if it changes
                if readings[i] is self.OK:
                    pygame.draw.rect(self.screen, self.GREY,pygame.Rect(self.imgPositions[i], (128, 128))) #Draw a rect over it
                    self.screen.blit(self.okImg, self.imgPositions[i])
                    self.sonars[i] = self.OK
                elif readings[i] is self.CLOSE:
                    pygame.draw.rect(self.screen, self.GREY,pygame.Rect(self.imgPositions[i], (128, 128))) #Draw a rect over it
                    self.screen.blit(self.warnImg, self.imgPositions[i])
                    self.sonars[i] = self.CLOSE
                    pygame.mixer.music.play() #Play warning sound
                elif readings[i] is self.FAR:
                    pygame.draw.rect(self.screen, self.GREY,pygame.Rect(self.imgPositions[i], (128, 128))) #Draw a rect over it
                    self.screen.blit(self.qImg, self.imgPositions[i])
                    self.sonars[i] = self.FAR        
        pygame.display.flip()

