# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 22:01:48 2021

@author: user
"""

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

class server:
   
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.RunServer(self)
        self.launch = True
        self.recvData = threading.Thread(target=self.recvData,args=())#чат
        self.command = threading.Thread(target=self.comandPromt,args=())#команды
        self.command.start()


    def Send_to_client(self):
        while self.launch:
            while not self.recvPackets.empty(): 
                self.data,self.addr = self.recvPackets.get()
                if self.addr not in self.clients: #новый клиент
                    self.clients.add(self.addr)
                    self.filter_for_chat(self.addr)
                    continue
                self.clients.add(self.addr)
                self.data = self.data.decode('utf-8') 
    
                if self.data.endswith('qqq'): 
                    self.clients.remove(self.addr)
                    continue
                chat=str(self.addr)+self.data
                print(chat)
                self.write_logs(chat)
                for c in self.clients: 
                    if c!=self.addr: 
                        self.s.sendto(self.data.encode('utf-8'),c) 
        self.s.close()


    def write_logs(self,data): #запись сообщений в документ(сохранение логов)
        f=open('log.txt','a')
        date=f"{datetime.now().month}.{datetime.now().day} {datetime.now().hour}:{datetime.now().minute}"
        date+=data
        date+="\n"

        f.write(date)


    def filter_for_chat(self,client): # фильтрация сообщений
        f = open ("1.txt", "rb")
        l = f.read(1024)
        while (l):
             try:
                 self.s.sendto(l,client)
             except BaseException:
                 print("Не удалось отправить данные фильтра...")
             l = f.read(1024)
        f.close()


    def comandPromt(self):
         while True:
             command=(str(input("Введите команду")))
             if (command == 'rm'):
                try:
                    addr=str(input())
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
                      self.recvData.join()
                      self.launch = False
                      break
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
                 data="CHANGE_PORT_"+data
                 for c in self.clients:
                     self.s.sendto(data.encode('utf-8'),c)
                 self.recvData.join(5)
                 self.s.close()
                 self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                 self.s.bind((self.host,new_port))
                 self.recvData.start()
                 print(self.s)
             if(command == "f"):
                 
                    for c in self.clients:
                      try:
                          self.filter_for_chat(c)
                          print("Успешно отправил все фильтры")
                      except:
                          print("Фильтр не отправился")

    def decode_data(data,test):
        if(test == 1): #decode
            data = data.decode_data('utf-8')
            return data
        if(test == 2):
            data=data.encode('utf-8')
            return data    

    def RunServer(self,self1,port=5002):#port по умолчанию
      #  @staticmethod
        self.host = socket.gethostbyname(socket.gethostname())

        self.clients=set()
        print('Server hosting on IP-> '+str(self.host))
        self.s.bind((self.host,port))
        self.recvPackets = queue.Queue()
        print('Server Running...')

    def recvData(self):#получаем данные
        while self.launch:
            #print(self.s)
            try:
                self.data, self.addr = self.s.recvfrom(1024) #получаем даные от сокета
                self.recvPackets.put((self.data,self.addr))
            except:
                pass
if __name__ == '__main__':
    server =  server()
    server.Send_to_client()


