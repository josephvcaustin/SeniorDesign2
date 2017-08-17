import os, sys, socket
from time import sleep

class Client:

    def __init__(self):
        self.sock = socket.socket()
        self.host = ""
        self.port = ""
        fileName = "IP.txt"
        if os.path.isfile(fileName):
            lines = open(fileName).readlines()
            self.host = lines[0].strip()
            self.port = int(lines[1].strip())
        else:
            self.host = raw_input("IP: ") #IP to connect to
            self.port = int(raw_input("Port: ")) #Doesn't seem to really matter

        print "Connecting to {} : {} ...".format(self.host, self.port)
        self.sock.connect((self.host, self.port))
        #Server will send a message that connection was successful.
        #Receive the message and print it out.
        print self.sock.recv(1024)
        self.sock.setblocking(0)
        self.sock.settimeout(0)

    def send(self, value):
        self.sock.send(value)

    def reconnect(self):
        self.sock.close()
        self.sock = None
        self.sock = socket.socket()
        print "Retrying..."
        self.sock.setblocking(0)
        self.sock.settimeout(1)
        while True:
            try:
                self.sock.connect((self.host, self.port))
                print self.sock.recv(1024)
                self.sock.setblocking(0)
                self.sock.settimeout(0)
                return True
            except:
                return False

#client = Client()
#client.send("Hi server!")
