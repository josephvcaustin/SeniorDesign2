import os

os.system("sudo ./stop.sh")     #stop camera stream, script file.sh must py in same directory
os.system("sudo ./start.sh")    #start camera stream, script file.sh must py in same directory
os.system("sudo pigpiod")       #start pigpio daemon, must be done to use gpio library
