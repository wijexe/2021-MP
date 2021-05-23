import socket
import threading
import queue
import sys
import random
import os
import logging
import time
import csv


from settings import PORT,BUFFERSIZE,ENCODING

logger=logging.getLogger('main')   #логирование
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler=logging.FileHandler('info.log',encoding=ENCODING)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)    
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

BufferSize=BUFFERSIZE
encoding=ENCODING
port=PORT

class Server():
    def __init__(self, host, socket):
        self.port = port
        self.host = host
        self.socket = socket

    def RunServer(self):         
        clients = set()
        recvPackets = queue.Queue()

        threading.Thread(target=RecvData,args=(self.socket,recvPackets)).start()

        while True:
            while not recvPackets.empty():
                data,addr = recvPackets.get()
                if addr not in clients:
                    clients.add(addr)
                    with open('list.csv', 'w', newline='') as file: #список клиентов
                        csv.writer(file).writerow(clients)
                    continue
                clients.add(addr)
                itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                data = data.decode(encoding) 
                data=CringeFilter(data)  #вызов фильтра 
                if data.endswith('/exit'):
                    clients.remove(addr)
                    continue
                # print('['+str(addr[0])+']'+'='+'['+str(addr[1])+']'+'='+'['+itsatime+']'+'/'+data)
                logger.info('['+str(addr[0])+']'+'='+'['+str(addr[1])+']'+'='+'['+itsatime+']'+'/'+data)
                for c in clients:  #клиент не получает свои сообщения
                    if c!=addr:
                        self.socket.sendto(data.encode(encoding),c)

def change_port():
    print('*'*53)
    port=int(input('Enter new port: '))
    print('*'*53)
    logger.info('Server change port = ' + str(port))
    main(port)

def commands():
    while True: 
        command=input("Server: ")
        if command=='/change port':
            change_port(logger)
        elif command=='/clients':
            with open('list.csv', 'r', newline='') as file:
                reader=csv.reader(file)
                for row in reader:
                    print(row)
        elif command=='/help':
            with open('help.txt',encoding='utf-8',newline='') as file:
                print(file.read()) 
        elif command=='/exit':
            break
                
def create_server(port):
    host = socket.gethostbyname(socket.gethostname())

    print('='*53)
    print('*'*18+'Server Running'+'*'*21)
    print('='*53)
    print('Server hosting on IP -> ['+str(host)+'] Port -> ['+str(port)+']')  
    logger.info('Server hosting on IP -> ['+str(host)+'] Port -> ['+str(port)+']') 
    print('='*53)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    return (host, s)

def CringeFilter(data):   #фильтр слов 
    filterword=str(input('Enter the word you want to filter: '))
    replacement=str(input('Enter filter: '))
    data=data.replace(filterword,replacement)
    data=data.replace('cringe','maybe cring')
    data=data.replace('Cringe','maybe cring')
    data=data.replace('died of cringe','cringan kaytis boldin')
    return data

def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))
        
def main(port):
    # logger = create_logger()
    srv = create_server(port)
    server = Server(srv[0], srv[1])
    try:
        server.RunServer()
    except:
        logger.info('Server closed')
        print('Server closed')

# if __name__ == "__main__":
if len(sys.argv)==1:
    main(port)
elif len(sys.argv)==2:
    commands()


