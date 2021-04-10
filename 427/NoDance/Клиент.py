from socket import *
from threading import Thread
import time as ti

# Клиент
class Client():
    def __init__(self): # Запуск клиента, ввод ника
        # внести всю эту рутину в отдельный класс и вызвать например startClientSocket('localhost', self.port)
        self.host='127.0.0.1' ; self.port=3000 ; self.b_size=1024
        self.sockaddr=(self.host,self.port) ; self.title="Выйти"
        self.client=socket(AF_INET,SOCK_DGRAM)
        #self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.nick=input("Введите ник: ")
        nick_msg="n_"+self.nick
        # внести это тоже в connectToServer, или вставить в startClientSocket
        self.client.sendto(nick_msg.encode('utf-8'),self.sockaddr)
        self.run=True
        
        
    def Look(self): # Просмотр чата в отдельном потоке
        while self.run:
            try:
                ti.sleep(0.1)
                # recieveMsg()
                data,addr = self.client.recvfrom(self.b_size)
                w_data=data.decode('utf-8')
                if w_data.startswith('*_'):
                    i=2 ;tmp=""
                    while i<len(w_data):
                        tmp+=w_data[i]
                        i+=1
                    w_data=tmp
                    print(w_data)
                    self.run=False
                else:
                    print(w_data)
                ti.sleep(0.1)
            except:
                pass
    
    def Chat(self): # Отправка сообщений
        while self.run:
            data=input()
            # if isCommand(data): doCommand(data)
            if data.startswith('/Client.SwitchNick'):
                i=19 ; tmp=""
                while i<len(data):
                    tmp+=data[i]
                    i+=1
                data="sn_"+tmp
                self.client.sendto(data.encode('utf-8'),self.sockaddr)
                ti.sleep(0.1)
            else:
                # sendMsg()
                d=data.encode('utf-8')
                self.client.sendto(d,self.sockaddr)
                if data.endswith('qqq'):
                    self.client.close()
                    self.run=False
                    ti.sleep(0.1)
a=Client()
Thread(target=a.Look).start()
Thread(target=a.Chat).start()
