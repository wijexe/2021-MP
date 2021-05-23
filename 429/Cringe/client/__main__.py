import socket
import threading
import queue
import sys
import random
import os
import time


from settings import ENCODING,BUFFERSIZE


class Client:

    def __init__(self):
        self.name = None
        self.port = random.randint(6000, 8000)
        self.serverIP = '192.168.56.1'

    def ReceiveData(self,sock,encoding,BufferSize):
        while True:
            try:
                data,addr = sock.recvfrom(BufferSize)
                data=data.decode(encoding)
                itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                print('['+str(addr[0])+']'+'='+'['+str(addr[1])+']'+'='+'['+itsatime+']'+'/'+data)
            except:
                pass

    def Rename(self):
        print('*'*53)
        name=input("Enter new name: ")
        print('*'*53)
        self.name = name     
        return self.name

    def Connect(self):
        print('*'*53)
        serverIP=input('Enter new serverIP: ')
        port=int(input('Enter new port: '))
        print('*'*53)
        self.port = port
        self.serverIP = serverIP
        self.RunClient(self.serverIP,self.port)

    def RunClient(self, serverIP, port):
        if port != None:
            self.port = port
        if serverIP != None:
            self.serverIP = serverIP
        
        BufferSize=BUFFERSIZE
        encoding=ENCODING
        host = socket.gethostbyname(socket.gethostname())

        with open('Cringe.txt',encoding='utf-8',newline='') as file:
            print(file.read())
        print('='*100)
        print('*'*40+'Client Running'+'*'*46)
        print('='*100)
        print(' '*27+'Client IP -> ['+str(host)+'] Port -> ['+str(self.port)+']')
        print('='*100)
        server = (str(self.serverIP),8000)
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((host,self.port))
        s.setblocking(0)

        join=False

        name = input('Please write your name here: ')
        if name == '':
            name = 'Guest'+str(random.randint(1000,9999))
            #logger.info('Your name is:'+name) 
            print('Your name is:'+name)
        s.sendto(name.encode(encoding),server)

        recvPackets = queue.Queue()
        threading.Thread(target=self.ReceiveData,args=(s,encoding,BufferSize)).start()

        while True:
            if join == False:
                data='['+ name + '] -> join chat'
                s.sendto(data.encode(encoding),server)
                join=True
            data = input()
            if data == '/exit':
                break
            elif data=='':
                continue
            elif data=='/rename':
                old_name=name
                name=self.Rename()
                data= '['+old_name+']' + ': change name'+' on ' + '['+name+']'
                s.sendto(data.encode(encoding),server)
            elif data=='/connect':
                data='['+name+']' + ' <- ' + 'left the chat' 
                s.sendto(data.encode(encoding),server)
                self.Connect()
            elif data=='/help':
                with open('help.txt',encoding='utf-8',newline='') as file:
                    print(file.read())
            else:
                data = '['+name+']' + ' -> '+ data
                s.sendto(data.encode(encoding),server)
            # data,addr = sock.recvfrom(1024)
            # recvPackets.put((data,addr))
            # data,addr = recvPackets.get()
            # data = data.decode(encoding)
            # print(data)
        data='['+name+']' + ' <- ' + 'left the chat' 
        s.sendto(data.encode(encoding),server)
        s.close()
        os._exit(1)
      
def main():
    client = Client()
    try:
        client.RunClient(sys.argv[1],int(sys.argv[2]))
    except:
        pass

# if __name__ == "__main__":
main()