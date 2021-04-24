import threading
import random
import time

class FileExecutor():
    def writeDown_name(self, name):   
        f = open('name.txt', 'a')
        f.write(name + '\n')
        f.close()
    def writeDown_log(self, data):
        f = open('data.txt', 'a')
        f.write(time.ctime() + data + '\n')
        f.close()
class Filter():   
    def addBanWord(self, data):
        for line in self.showBanList():
            if data.lower() == line:
                return          
        f = open('banWords.txt', 'a')
        f.write(data.lower() + '\n')
        f.close()
                
    def showBanList(self):
        f = open('banWords.txt', 'r')
        lines = f.read().splitlines()
        return lines 
    def censor(self, data, name):
        for line in self.showBanList():
            if data.lower().endswith(line.lower()):
                print("Don't swear")
                data = '*****'
                break
        data = '['+name+']' + '->'+ data
        return data
class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def getHost(self):
        return self.host
    def getPort(self):
        return self.port
        
    def receive(self, client, server):
        while True:
            try:
                data,addr = client.recvfrom(1024)
                print(data.decode('utf-8'))
            except:
                print("An error occured!")
                client.close()
                break           
    def write(self, client, server):
        filter_class = Filter()
        fileExecutor = FileExecutor()
        name = input('Choose your nickname: ')
        if name == '':
            name = 'Guest'+str(random.randint(1000,9999))
        print('Your name is:'+name)
        fileExecutor.writeDown_name(name)
        client.sendto(name.encode('utf-8'),server)
        while True:
            data = input()
            if data == 'qqq':
#               client.sendto(data.encode('utf-8'),server)
                break
                
            elif data=='':
                continue
                
            elif data == '/addBanWord':
                ban = input()
                filter_class.addBanWord(ban)
                continue
                
            elif data == '/showBanWords':
                print ("These words are forbidden to use: ", filter_class.showBanList())
                continue     
            data = filter_class.censor(data, name) 
            fileExecutor.writeDown_log(data)
            client.sendto(data.encode('utf-8'),server)
        message = name + " live the chat!"
        client.sendto(message.encode('utf-8'),server)    
        client.close()
        
    def runClient(self):
        pass
        client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client.bind((self.getHost(),self.getPort())) 
        print('Client IP->'+str(self.getHost())+' Port->'+str(self.getPort()))
        server = (str(self.getHost()),5000)
        
        receive_thread = threading.Thread(target=self.receive, args=(client, server))
        receive_thread.start()
        write_thread = threading.Thread(target=self.write, args=(client, server))
        write_thread.start()
        
        
        
myHostName = socket.gethostname()
host = socket.gethostbyname(myHostName)
port = random.randint(6000,10000)   
client = Client(host, port)
client.runClient()
