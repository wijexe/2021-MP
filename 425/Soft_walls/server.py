import socket # библиотека для обмена сокетами
import threading
import queue





class Server:
    def start(self):
        self.sct = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5000
        self.sct.bind((self.host, self.port))
        self.SctIsnRun = False
        
        print('\nServer hosting on IP: ' + str(self.host))
        print('Server running...\n')

        
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

        while True:
            if sctrn():
                break
            try:
                if not dubl.empty():
                    data,addr = dubl.get()
                    if addr not in self.clients:
                        self.clients.add(addr)
                        continue
                    data = data.decode('utf-8')

                    if data.endswith('/quit'):
                        self.clients.remove(addr)
                        continue

                    for c in self.clients:
                        if c != addr:
                            sock.sendto(data.encode('utf-8'), c)
            except: 
                pass
    def startCBase(self, sock, sctrn):
        self.clients = set()
        self.dublet = queue.Queue()
        self.thrdRcv = threading.Thread(target=self.receiver, args=(sock, sctrn, self.dublet,))
        self.thrdRcv.start()
    def stopCBase(self):
        self.thrdRcv.join()

def RunServer():
    s = Server()
    cb = ClientsBase()
    s.start()
    cb.startCBase(s.getSocket(), lambda: s.getSctIsnRun())

    while True:
        inp = input('TF Console: ')

        if inp == '/restart':
            s.stop()
            cb.stopCBase()
            s.start()
            cb.startCBase(s.getSocket(), lambda: s.getSctIsnRun())
        if inp == '/stop':
            s.stop()
            cb.stopCBase()
            break

        

            

            

            

        








        

    


            

            

