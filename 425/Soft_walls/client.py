#Перфилов Алексей, Васильев Леонид
import socket
import threading
import random
import os



class Client:
    def start(self):
        self.sct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = random.randint(6000, 10000)
        self.sct.bind((self.host, self.port))
        self.SctIsnRun = False
        
        print('\nClient IP: ' + str(self.host) + ' Port: ' + str(self.port))
        
    def stop(self):
        self.SctIsnRun = True
        self.sct.close()
        
        print('Client Closed')
        
    def getSocket(self):
        return self.sct
    
    def getSctIsnRun(self):
        return self.SctIsnRun
    
class DataControl:
    def receiver(self, sock, sctrn):
        while True:
            if sctrn():
                break
            try:
                data, addr = sock.recvfrom(1024)
                print(data.decode('utf-8'))             ####
            except: 
                pass
            
    def sender(self, sock, data):
        data = '[' + self.name + '] -> ' + data
        sock.sendto(data.encode('utf-8'), self.server)
        
    def setName(self):
        self.name = input()
            
    def startDC(self, sock, sctrn, IP, PRT):
        self.server = (str(IP), int(PRT))
        self.name = input('Your nickname: ')
        if self.name == '':
            self.name = 'Guest' + str(random.randint(1000, 9999))
            print('Your name is: ' + self.name)
        sock.sendto(self.name.encode('utf-8'), self.server)
        print(self.server)
        
        self.thrdRcv = threading.Thread(target = self.receiver, args = (sock, sctrn,))
        self.thrdRcv.start()
        
    def stopDC(self):
        self.thrdRcv.join()

def RunClient(IP, Port):
    c = Client()
    dc = DataControl()
    c.start()
    dc.startDC(c.getSocket(), lambda: c.getSctIsnRun(), IP, Port)
    
    while True:
        inp = input('TF Client: ')
        
        if inp == '/quit':
            dc.sender(c.getSocket(), inp)
            c.stop()
            dc.stopDC()
            break
        elif inp == '/reconnect':
            dc.sender(c.getSocket(), '/quit')
            c.stop()
            dc.stopDC()
            c.start()
            dc.startDC(c.getSocket(), lambda: c.getSctIsnRun(), input('IP: '), input('Port: '))
        elif inp == '/name':
            dc.setName()
        else:
            dc.sender(c.getSocket(), inp)
            
    os._exit(1)
