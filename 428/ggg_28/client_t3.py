import socket
import threading
import queue
import sys
import random
import os
import codecs

class Client():
    
    name = 'name'
    s ='s'
    #server = 'server'
    
    
    replaceable = [] #Заменяемое
    substitute = [] #Заменяющее
        
    def __init__(self, IP):
        global name, s
        self.server = 'server'
        self.IP = IP
        print (type(IP))
        self.RunHost(self.IP) #Запуск клиента
        self.ReadFilter()
        self.CheckName()
        self.recData = threading.Thread(target=self.ReceiveData,args=(s,))
        self.recData.start()
        self.StartThread()
        self.CheckMassage()
        self.recData = threading.Thread(target=self.ReceiveData,args=(s,))
        self.recData.start()
        
    def RunHost(self,serverIP):
        global s
        self.host = socket.gethostbyname(socket.gethostname())
        port = random.randint(6000,10000)
        print('Client IP->'+str(self.host)+' Port->'+str(port))
        self.server = (str(serverIP),5002)
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((self.host,port))
    
   
    def CheckName(self):
        global name, s
        name = input('Please write your name here: ')
        if name == '':
            name = 'Guest'+str(random.randint(1000,9999))
            print('Your name is:'+name)
        s.sendto(name.encode('utf-8'),self.server)
        self.ReadFilter()
        
        
    
    def ReceiveData(self,sock):
        global s
        while True:
            try:
                data,addr = sock.recvfrom(1024)
                if (addr[0] == self.IP):
                    if ( data.decode('utf-8') == "BRAKE_CONNECTIONS_"):
                        print("ВЫ БЫЛИ ОТКЛЮЧЕНЫ!")
                        s.close()
                        os._exit(1)
                        break
                    if ( data.decode('utf-8')[0:12] == "CHANGE_PORT_"):
                        print("Начинаем менять порт")
                        self.recData.join(5)
                        print("1", s)
                        port = int(data.decode('utf-8')[12:16])
                        print("Твой новый порт - ", port,s)
                        try:
                            self.server = (str(self.IP),int(port))
                        except:
                            print("Не удалось переназаначить порт")
                        print (self.server)
                    else:
                        self.ReadFilter()
                        print(data.decode('utf-8'))
                    print(data.decode('utf-8'))
            except:
                pass 
        
        
    def Filter(self,data):
        f = open("filter.txt", "w")
        f.write(data.decode('utf-8'))
        f.close()
        
    def StartThread(self):
        global s
        threading.Thread(target=self.ReceiveData,args=(s,)).start() #запускам поток с ф-циией ReceiveData
         
        
    def CheckMassage(self):
        global name, s
        while True:
            data = input("-->")
            data = self.FilterMassage(data)
            if data == 'qqq ':
                print ('Press q to exit the Chat\nEnter nick to change nickname\n')
                command = input()
                if command == 'q':
                    break
                elif command == 'nick':
                    self.CheckName()
            elif data=='':
                continue
            data = '['+name+']' + '->'+ data
            s.sendto(data.encode('utf-8'),self.server)
        s.sendto(data.encode('utf-8'),self.server)
        s.close()
        os._exit(1)

    def ReadFilter(self):
        global replaceable, substitute, IP
        fil = []
        f=codecs.open("filter.txt","r")
        idx = 0
        for line in f:
            for word in line.split():
                try:
                    fil.append(word)
                    idx += 1
                except:
                    continue
        f.close()
        rep = []
        sub = []
        for i in range(0,len(fil),2):
            rep.append(fil[i])
        for i in range(1,len(fil),2):
            sub.append(fil[i])
        replaceable = rep
        substitute = sub

        
    def FilterMassage(self,data):
        global replaceable, substitute
        self.data = data
        word = self.data.split()
        new_data = ''
        for i in range(len(word)):
            for j in range(len(replaceable)):
                if word[i] == replaceable[j]:
                    word[i] = substitute[j]
            new_data = new_data + word[i] + ' ' 
        return (new_data)




if __name__ == '__main__':
    IP = input("Введите IP: ")
    client = Client(IP)
