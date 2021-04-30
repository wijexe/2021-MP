import socket
import queue
import Filter
import File_Executor



class Server():
    def __init__(self, host, port,  recvPackets = queue.Queue()):
        self.host = host
        self.port = port
        self.recvPackets = recvPackets
        open('logs.txt', 'w').close()

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def getQueue(self):
        return self.recvPackets

    def receive(self, sock, recvPackets):
        fileExecutor = File_Executor.FileExecutor()
        filter_class = Filter.Filter()
        while True:
            data,addr = sock.recvfrom(1024)
            recvPackets.put((data, addr))
            fileExecutor.writeDown_log(filter_class.censor(data.decode('utf-8')))

    def runServer(self):
        pass
        print('Server hosting on IP-> '+str(self.getHost()))
        server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server.bind((self.getHost(),self.getPort()))
        print('Server Running...')
        self.receive(server, self.getQueue())

    def greetings(self,i):
        f = open('name.txt', 'r')
        lines = f.read().splitlines()
        name = lines[i]
        message = name + " joined the chat!"
        return message


host = socket.gethostbyname(socket.gethostname())
port = 5000
server = Server(host, port,)
server.runServer()

