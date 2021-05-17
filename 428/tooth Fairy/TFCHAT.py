import socket
import threading
import queue
from datetime import datetime as dt
import random
import os
import sys


###############################################################################
#SERVER
class Server:
    def start(self):
        self.sct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = int(input('Set Server Port: '))
        self.sct.bind((self.host, self.port))
        self.SctIsnRun = False
        
        print('\nServer hosting on IP: ' + str(self.host))
        print('Server running...\n')
        print('<< /help >> for more')
        
    def stop(self):
        self.SctIsnRun = True
        self.sct.close()
        
        print('Server Closed')
        
    def getSocket(self):
        return self.sct
    
    def getSctIsnRun(self):
        return self.SctIsnRun

class ClientsBase:
    def receiver(self, sock, sctrn, dubl):
        while True:
            if sctrn():
                break
            try:
                data, addr = sock.recvfrom(1024)
                dubl.put((data, addr))
            except: 
                pass
            
    def sender(self, sock, sctrn, dubl):
        log = open('TFlog.txt', 'a')
        while True:
            if sctrn():
                break
            try:
                if not dubl.empty():
                    data, addr = dubl.get()
                    data = data.decode('utf-8')
                    if addr not in self.clients:
                        self.clients.add(addr)
                        joinmsg = "<<<<<Hello! Welcome to Tooth Fairy Chat>>>>>\n<< /help >> for more"
                        sock.sendto(joinmsg.encode('utf-8'), addr)
                        if self.mode == 1:
                            print(dt.now().time().strftime('%H:%M:%S ') + str(addr) + ' [' + data + '] joined')
                            log.write(dt.now().time().strftime('%H:%M:%S ') + str(addr) + ' [' + data + '] joined\n')
                        continue
                    if data.endswith('/quit'):
                        self.clients.remove(addr)
                        continue
                    if self.mode == 1:
                        print(dt.now().time().strftime('%H:%M:%S ') + str(addr) + ' ' + data)
                        log.write(dt.now().time().strftime('%H:%M:%S ') + str(addr) + ' ' + data + '\n')
                    for c in self.clients:
                        if c != addr:
                            sock.sendto(data.encode('utf-8'), c)
            except: 
                pass
        log.close()
            
    def filterTF(self, sctrn, dubl, dublF, bans):
        while True:
            if sctrn():
                break
            try:
                if not dubl.empty():
                    data, addr = dubl.get()
                    data = data.decode('utf-8')
                    for b in bans:
                        if b in data:
                            nick = ''
                            for s in data:
                                if s == ']':
                                    break
                                else:
                                    nick += s
                            data = nick +'] Пошел чистить зубы!'
                            nick = ''
                    dublF.put((data.encode('utf-8'), addr))
            except: 
                pass
            
    def getFilter(self):
        print('Server Filter:') 
        if not self.ban:
            print('No Filters\n')
        else:
            for c in self.ban:
                print(c)
            print('\n')
            
    def setFilter(self):
        print('Set Server Filter:') 
        self.ban.append(input())
        print('\n')
        
    def rmvFilter(self):
        print('Remove Server Filter:')
        rmv = input()
        if rmv in self.ban:
            self.ban.remove(rmv)
            print('\n')
        else:
            print('Filter not found\n')
            
    def swhMode(self):
        self.mode *= -1
        print('Mode switched\n')
            
    def kick(self, sock, kicks):
        if kicks == '':
            for c in self.clients:
                sock.sendto('Server Closed'.encode('utf-8'), c)
        else:
            if self.clients:
                for c in self.clients:
                    if str(kicks) in str(c):
                        userKick = c
                sock.sendto('You kicked. Server lost...'.encode('utf-8'), userKick)
                self.clients.remove(userKick)
            else: 
                print('No Users\n')
            
    def startCBase(self, sock, sctrn):
        self.clients = set()
        self.dublet = queue.Queue()
        self.dubletF = queue.Queue()
        self.ban = ['Кариес', 'шоколад', 'конфеты', 'сладости', 'открывать бутылку зубами', 
                    'семечки', 'кофе', 'сигареты', 'карамель', 'ирис']
        self.mode = 1
        
        self.thrdRcv = threading.Thread(target = self.receiver, args = (sock, sctrn, self.dublet,))
        self.thrdSnd = threading.Thread(target = self.sender, args = (sock, sctrn, self.dubletF,))
        self.thrdFlt = threading.Thread(target = self.filterTF, args = (sctrn, self.dublet, self.dubletF, self.ban))
        self.thrdRcv.start()
        self.thrdSnd.start()
        self.thrdFlt.start()
        
    def stopCBase(self):
        self.thrdRcv.join()
        self.thrdSnd.join()
        self.thrdFlt.join()
        
def RunServer():
    s = Server()
    cb = ClientsBase()
    s.start()
    cb.startCBase(s.getSocket(), lambda: s.getSctIsnRun())
    
    while True:
        inp = input('TFS Console: ')
        
        if inp == '/restart':
            cb.kick(s.getSocket(), '')
            s.stop()
            cb.stopCBase()
            s.start()
            cb.startCBase(s.getSocket(), lambda: s.getSctIsnRun())
            
        if inp == '/help':
            print('<< /restart >> - restart Server\n<< /setf >> - set Filter')
            print('<< /getf >> - get Filter\n<< /rmvf >> - remove Filter')
            print('<< /kick >> - disconnect a user\n<< /m >> - switch Server Mode')
            print('<< /stop >> - stop Server\n')
            
        if inp == '/setf':
            cb.setFilter()
            
        if inp == '/getf':
            cb.getFilter()
        
        if inp == '/rmvf':
            cb.rmvFilter()
            
        if inp == '/kick':
            cb.kick(s.getSocket(), input())
            
        if inp == '/m':
            cb.swhMode()
            
        if inp == '/stop':
            cb.kick(s.getSocket(), '')
            s.stop()
            cb.stopCBase()
            break
###############################################################################


###############################################################################
#CLIENT
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
                if data.decode('utf-8') == 'You kicked. Server lost...':
                    print(dt.now().time().strftime('%H:%M:%S ') + data.decode('utf-8'))
                    self.online = False
                else:
                    print(dt.now().time().strftime('%H:%M:%S ') + data.decode('utf-8'))
            except: 
                pass
            
    def sender(self, sock, data):
        if self.online:
            data = '[' + self.name + '] >>> ' + data
            sock.sendto(data.encode('utf-8'), self.server)
        
    def setName(self):
        self.name = input()
            
    def startDC(self, sock, sctrn, IP, PRT):
        self.server = (str(IP), int(PRT))
        self.name = input('Your nickname: ')
        self.online = True
        if self.name == '':
            self.name = 'Guest' + str(random.randint(1000, 9999))
            print('Your name is: ' + self.name)
        sock.sendto(self.name.encode('utf-8'), self.server)
        
        self.thrdRcv = threading.Thread(target = self.receiver, args = (sock, sctrn,))
        self.thrdRcv.start()
        
    def getOnline(self):
        return self.online
    
    def stopDC(self):
        self.thrdRcv.join()

def RunClient(IP, Port):
    c = Client()
    dc = DataControl()
    c.start()
    dc.startDC(c.getSocket(), lambda: c.getSctIsnRun(), IP, Port)
    
    while True:
        if dc.getOnline():
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
            elif inp == '/help':
                print('<< /name >> - new nickname\n<< /reconnect >> - set new connecting parameters')
                print('<< /quit >> - disconnect\n')
            else:
                dc.sender(c.getSocket(), inp)
        else:
            dc.sender(c.getSocket(), '/quit')
            c.stop()
            dc.stopDC()
            c.start()
            dc.startDC(c.getSocket(), lambda: c.getSctIsnRun(), input('IP: '), input('Port: '))
            
    os._exit(1)
###############################################################################


if __name__ == '__main__':
    if len(sys.argv) == 1:
        RunServer()
    elif len(sys.argv) == 3:
        RunClient(sys.argv[1], sys.argv[2])
    else:
        print('Run Server >>> chat.py')
        print('Run Server >>> chat.py IP Port')