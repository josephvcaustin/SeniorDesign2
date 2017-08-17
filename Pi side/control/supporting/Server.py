#Server.py
#Opens a socket for communication
#with the operator. Handles restarting
#server after loss of signal.
import sys, socket, fcntl, struct
from time import sleep
import SocketServer
import smtplib
SocketServer.TCPServer.allow_reuse_address = True
SocketServer.UDPServer.allow_reuse_address = True
DEFAULT_TIMEOUT = 0 #heartbeat every 1 second
class Server:
    def waitForClient(self):
        self.sock.close()
        sleep(1)
        self.sock = socket.socket()
        self.host = self.get_ip_address("wlan0")
        port = 12345 #Doesn't seem to really matter
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, port))
        self.sock.settimeout(None)
        self.c.settimeout(None)
        self.sock.listen(1)
        self.c, self.addr = self.sock.accept() #Sit here and wait for a client.
        print "Client connected from", self.addr
        self.c.send('Reconnected to server.')
        #Set the timeout for the heartbeat signal
        self.sock.settimeout(DEFAULT_TIMEOUT)
        self.c.settimeout(DEFAULT_TIMEOUT)
    #Automatically determine the IP address from the Pi's WLAN
    def get_ip_address(self, ifname):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return socket.inet_ntoa(fcntl.ioctl(
            self.s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    def sendEmail(self): #Send email with IP to connect to
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("rpi.capstone4b@gmail.com", "capstone4b")
        msg = "Catch a ride at {} !".format(self.host)
        recepients = ["josephvcaustin@gmail.com"]
        server.sendmail("rpi.capstone4b@gmail.com", recepients, msg)
        server.quit() 
    def start(self):
        #Call start() again if an exception occurs.
        #Close anything that was opened.
        if self.sock is not None:
            self.sock.close()
            self.sock = None
        if self.s is not None:
            self.s.close()
            self.s = None
        if self.c is not None:
            self.c.close()
            self.c = None
        try:
            self.sock = socket.socket()
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.host = self.get_ip_address("wlan0")
            self.s.close() #s is only used to get the IP
            port = 12345 #Doesn't seem to really matter
            self.sock.bind((self.host, 12345))
            self.sock.settimeout(None)
        except Exception as inst:
            print "Failed to bind socket: {}".format(inst)
            sleep(1)
            self.start()
##        try: self.sendEmail()
##        except Exception as inst:
##            print "Failed to send email: {}".format(inst)
##            sleep(1)
        a = False
        while(not a):
            try:
                self.sock.listen(5) #Only accept one client
                print "Starting server at", self.host, ": 12345"
                self.c, self.addr = self.sock.accept() #Sit here and wait for a client.
                a = True
                break
            except Exception as inst:
                print "Failed listening for client: {}".format(inst)
                err = "{}".format(inst)
                if "[Errno 11]" in err:
                    print "Passing errno 11."
                    a = True
                    pass
                else:
                    sleep(5)
                    continue   
        print "Client connected from", self.addr
        self.c.send('Successfully connected to server.')
        #Set the timeout for the heartbeat signal
        self.sock.settimeout(DEFAULT_TIMEOUT)
        self.c.settimeout(DEFAULT_TIMEOUT)
        return 
    def __init__(self):
        SocketServer.TCPServer.allow_reuse_address = True
        SocketServer.UDPServer.allow_reuse_address = True
        self.s = None
        self.sock = None
        self.host = None
        self.c = None
        self.addr = None
        self.start()
        
