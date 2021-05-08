import socket
import Filter
import File_Executor
import Moderations

class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        open('logs.txt', 'w').close()

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def receive(self, sock):
        fileExecutor = File_Executor.FileExecutor()
        filter_class = Filter.Filter()
        moderator = Moderations.Moderator()
        while True:
            data,addr = sock.recvfrom(1024)
            name = filter_class.censor(data.decode('utf-8')).split(' ')[0][1:-1]
            clients = moderator.create_data(name)
            if filter_class.censor(data.decode('utf-8')).endswith("/admin"):
                clients = moderator.become_an_admin(name)
                fileExecutor.writeDown_log(name + ' ' + "become an administrator")
                continue
            moderator.admin(name, filter_class.censor(data.decode('utf-8')))
            if clients[name][0][0]:
                continue
            fileExecutor.writeDown_log(filter_class.censor(data.decode('utf-8')))

    def runServer(self):
        pass
        print('Server hosting on IP-> '+str(self.getHost()))
        server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        server.bind((self.getHost(),self.getPort()))
        print('Server Running...')
        self.receive(server)


host = socket.gethostbyname(socket.gethostname())
port = 5000
server = Server(host, port,)
server.runServer()


