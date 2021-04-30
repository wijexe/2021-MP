import socket # библиотека для обмена сокетами
import threading
import queue
import datetime
import sys # библиотека для работы с системными функциями
import random # библиотека для работы с рандомом
import os # библиотека для работы с операционной системой


def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))
#f = open('log.txt','w')
host = socket.gethostbyname(socket.gethostname())
port = 5000
print('Server hosting on IP-> '+str(host))
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
tm = datetime.datetime.today().strftime("%d-%m-%Y")
with open('logs.txt', 'a') as file:
    file.write('\n'+'__________'+tm+'__________'+'\n')
clients = set()
recvPackets = queue.Queue()

print('Server Running...\nConnection complete.')

threading.Thread(target=RecvData,args=(s,recvPackets)).start()

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