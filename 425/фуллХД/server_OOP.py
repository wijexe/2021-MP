import socket # библиотека для обмена сокетами
import threading
import queue
import datetime
import sys # библиотека для работы с системными функциями
import random # библиотека для работы с рандомом
import os # библиотека для работы с операционной системой 


host = socket.gethostbyname(socket.gethostname())
port = 5000
recvPackets = queue.Queue()

class Server:
    def __init__(self, host, port,  recvPackets):
        self.host = host
        self.port = port
        self.recvPackets = recvPackets
    
    def RecvData(self,sock,recvPackets):
        while True:
            data,addr = sock.recvfrom(1024)
            recvPackets.put((data,addr))
    #f = open('log.txt','w')
    
    
    def RunServ(self):#,host,port,recvPackets):
        print('Server hosting on IP-> '+str(self.host))
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((self.host,self.port))
        tm = datetime.datetime.today().strftime("%d-%m-%Y runtime-%H:%M")
        with open('logs.txt', 'a') as file:
            file.write('\n'+'__________'+tm+'__________'+'\n')
        clients = set()
        print('Server Running...\nConnection complete.')
        
        threading.Thread(target=self.RecvData,args=(s,recvPackets)).start()
        
        while True:
            while not recvPackets.empty():
                data,addr = recvPackets.get()
                if addr not in clients:
                    clients.add(addr)
                    continue
                clients.add(addr)
                data = data.decode('utf-8')
                if data.endswith('qqq'):
                    clients.remove(addr)
                    continue
                r = str(addr)+' '+data
                print(r)
                with open('logs.txt', 'a') as file:
                    file.write(r+'\n')
                for c in clients:
                    if c!=addr:
                        s.sendto(data.encode('utf-8'),c)
        s.close()


server = Server(host, port, recvPackets)
server.RunServ()


