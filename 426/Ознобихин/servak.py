import socket
import threading
import queue
from datetime import datetime
from sys import getsizeof
import sys
import random
import os
import time
import codecs

class Server:
    
    
    def __init__(self):#аки Handler
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#тип объекта Socket, AF_INET- семейство адрессов интернета, DGRAM протокол UPD
       # print(self.)
        self.RunServer(self)
        self.launch = True
        self.recvData = threading.Thread(target=self.recvData,args=())
        self.command = threading.Thread(target=self.comandPromt,args=())
        self.command.start()
        
       # print(self.launch)
        
       # threading.Thread(target=self.comandPromt().start())
        
        self.Send_to_client()
        #192.168.43.190
        
    def comandPromt(self):
         while True:
             command=(str(input("Введите команду")))
             if (command == 'rm'):
                try:
                    addr=str(input())
                   # print(type(self.clients[0]))
                    for adr in self.clients:
                        if (adr[0] == addr):
                            print(f"Я отключил {addr}")
                            self.clients.remove(adr)
                            data="BRAKE_CONNECTIONS_"
                            self.s.sendto(data.encode('utf-8'),adr)
                except BaseException:
                    print("Не удалось отключить клиента")
                    
             if (command == 'exit'):
                 try:
                      self.s.close()
                     # if (self.recvData.is_alive() == True):
                      self.recvData.join()
                      self.launch = False
                      break
                      #raise SystemExit(1)
                      sys.exit(0)
                 except BaseException:
                    print("Не удалось закрыть сокет...")
                    
             if (command == 's'):
                 try:
                     self.recvData.start()
                     print("Сервер успешно запущен...")
                 except BaseException:
                    print("Не удалось запустить сервер...")     
                    
             if(command == "cp"):# Change Port
                 new_port=int(input("Введите новый порт"))
                 data=str(new_port)
                 # for c in self.clients:
                 #     self.s.sendto(data.encode('utf-8'),c)
                 data="CHANGE_PORT_"+data
                 for c in self.clients:
                     self.s.sendto(data.encode('utf-8'),c)
                 self.recvData.join(5)
                 self.s.close()
                 self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                 self.s.bind((self.host,new_port))
                 #self.recvData.start()
                 print(self.s)
             if(command == "f"):
                 
                    for c in self.clients:
                      try:
                          self.filter_for_chat(c)
                          print("Успешно отправил все фильтры")
                      except:
                          print("Не смог отправить все фильтры")
                 
            
                    
    def RunServer(self,self1,port=5002):#port по умолчанию
      #  @staticmethod
        self.host = socket.gethostbyname(socket.gethostname())#переводи имя хоста в ip аддрес
        #gethostname вернуть имя хоста на которой выполняется эта команад
        self.clients=set() # перменная clients тип- множество
        print('Server hosting on IP-> '+str(self.host))
        self.s.bind((self.host,port)) # говорим системе мол дай забинлю этот порт
        self.recvPackets = queue.Queue() # переменная тип очереди FIFO
        print('Server Running...')

         # запускаем поток ф-ции RecvData
         
    def recvData(self):#получаем данные
        while self.launch:
            #print(self.s)
            try:
                self.data, self.addr = self.s.recvfrom(1024) #получаем даные от сокета
                self.recvPackets.put((self.data,self.addr))
            except:
                pass
   
    def decode_data(data,test):
        if(test == 1): #decode
            data = data.decode_data('utf-8')
            return data
        if(test == 2):
            data=data.encode('utf-8')
            return data
        
    def Send_to_client(self):
        while self.launch:
            while not self.recvPackets.empty():
                self.data,self.addr = self.recvPackets.get()# возвращает 2 штуки, первая данные, вторая аддресс
              #  print(type(self.addr[0]))
                if self.addr not in self.clients: # если адреса нет в клиентах то добавляем его
                    self.clients.add(self.addr)
                    self.filter_for_chat(self.addr)#если видим клиента первый раз то отправялем ему инфу из filter.txt
                    continue
             #   for adr in self.clients:
                   # print(adr[0])
                self.clients.add(self.addr) # и почему то делаем это опять?????
                self.data = self.data.decode('utf-8')  #декодим данные в utf 
                if self.data.endswith('qqq'): # если последние символы qqq то выход, и удаляем клиента
                    self.clients.remove(self.addr)
                    continue
                chat=str(self.addr)+self.data
                print(chat)# печатаем кто и что ответил
                self.write_logs(chat)
                for c in self.clients: # для всех cliеtn 
                    if c!=self.addr: # если c не тот клиент кто отправил сообщение то
                        self.s.sendto(self.data.encode('utf-8'),c) # передаем ему это сообщение
        self.s.close()

    def write_logs(self,data):
        f=open('log.txt','a')
        date=f"{datetime.now().month}.{datetime.now().day} {datetime.now().hour}:{datetime.now().minute}"
        date+=data
        date+="\n"
        #_time=time.clock()s
        #_time+=data
       # with open('log.txt', 'a') as f:
        #f.write(data)
            #f.writelines(lines)
        f.write(date)
        
    def filter_for_chat(self,client):
        #file = open("filter.txt", "r")
        f = open ("1.txt", "rb")
        l = f.read(1024)
        while (l):
             try:
                 self.s.sendto(l,client)
             except BaseException:
                 print("Не удалось отправить данные фильтра...")
             l = f.read(1024)
        f.close()
       
        
        
        
#Server Code
# def RecvData(sock,recvPackets):
#     while True:
#         data,addr = sock.recvfrom(1024) #получаем даные от сокета
#         recvPackets.put((data,addr))

# def RunServer():
#     host = socket.gethostbyname(socket.gethostname())#переводи имя хоста в ip аддрес
#     #gethostname вернуть имя хоста на которой выполняется эта команад
#     port = 4998
#     print('Server hosting on IP-> '+str(host))
#     s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #тип объекта Socket, AF_INET- семейство адрессов интернета, DGRAM протокол UPD
#     s.bind((host,port)) # говорим системе мол дай забинлю этот порт
#     clients = set() # перменная clients тип- множество
#     recvPackets = queue.Queue() # переменная тип очереди FIFO

#     print('Server Running...')

#     threading.Thread(target=RecvData,args=(s,recvPackets)).start() # запускаем поток ф-ции RecvData

#     while True:
#         while not recvPackets.empty():
#             data,addr = recvPackets.get()# возвращает 2 штуки, первая данные, вторая аддресс
#             if addr not in clients: # если адреса нет в клиентах то добавляем его
#                 clients.add(addr)
#                 continue
#             clients.add(addr) # и почему то делаем это опять?????
#             data = data.decode('utf-8')  #декодим данные в utf 
#             if data.endswith('qqq'): # если последние символы qqq то выход, и удаляем клиента
#                 clients.remove(addr)
#                 continue
#             print(str(addr)+data)# печатаем кто и что ответил
#             for c in clients: # для всех cliеtn 
#                 if c!=addr: # если c не тот клиент кто отправил сообщение то
#                     s.sendto(data.encode('utf-8'),c) # передаем ему это сообщение
#     s.close()
# #Serevr Code Ends Here

if __name__ == '__main__':
    server =  Server()
    # if len(sys.argv)==1:
    #     RunServer()
    # elif len(sys.argv)==2:
    #     RunClient(sys.argv[1])
    # else:
    #     print('Run Serevr:-> python Chat.py')
    #     print('Run Client:-> python Chat.py <ServerIP>')
