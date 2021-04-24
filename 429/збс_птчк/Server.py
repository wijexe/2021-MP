import socket
from tkinter import *
import threading, time

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 50050
SERVER_ADDR = (SERVER_IP, PORT)
CONN_ADDR = (SERVER_IP, PORT-1)
FORMAT = 'utf-8'
TITLE = 'Server'
SIZE = '400x300'

class Server:
    def __init__(self, ip=SERVER_IP, port=PORT):
        self._ip = ip
        self._port = port
        self._sock = 0

    def RunSocket(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self._sock.bind(self.getAddress())
            self._sock.setblocking(False)
            print('Socket runned')
            print(f'[CURRENT SERVER ADDRESS] {self.getAddress()}')
        except:
            print('[ERROR] Socket startup error\n')

    def CloseSocket(self):
        self.getSocket().shutdown(socket.SHUT_RDWR)
        self.getSocket().close()
        print('Socket closed')

    def getSocket(self):
        return self._sock

    def setAddres(self, ip, port):
        self._ip = ip
        self._port = port
        self.CloseSocket()
        print('Restarting socket...')
        self.RunSocket()
    
    def setIP(self, ip):
        self._ip = ip
        self.CloseSocket()
        print('Restarting socket...')
        self.RunSocket()

    def setPort(self, port):
        self._port = port
        self.CloseSocket()
        print('Restarting socket...')
        self.RunSocket()

    def getAddress(self):
        return self._ip, self._port
    
    def getIP(self):
        return self._ip

    def getPort(self):
        return self._port


class Connections:
    def __init__(self, addr=CONN_ADDR):
        self._addr = addr
        self._sock = 0

    def RunSocket(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self._sock.bind(self.getAddress())
            self._sock.setblocking(False)
            print('The server is waiting for clients')
        except:
            print('[ERROR] Connections socket startup error\n')

    def getSocket(self):
        return self._sock

    def getAddress(self):
        return self._addr
    
    def getIP(self):
        return self._addr[0]

    def getPort(self):
        return self._addr[1]


class ServerWindow:
    def __init__(self, title=TITLE, size=SIZE):
        self._tk = Tk()
        self._tk.title(title)
        self._tk.geometry(size)
        
    def getTK(self):
        return self._tk


class ClientsData:
    def __init__(self, name, addr):
        self._nickname = name
        self._addr = addr

    def getData(self):
        return (self._nickname, self._addr)

    def getNickname(self):
        return self._nickname

    def getAddress(self):
        return self._addr


class ClientsList:
    def __init__(self):
        self._clients = set()

    def recvClients(self, sock):
        thread = threading.currentThread()
        # using getattr to stop the looping thread correctly
        while getattr(thread, "do_run", True):
            try:
                name, addr = sock.recvfrom(1024)
                name = name.decode(FORMAT)
                clients = self.getClients()

                if name == '!DISCONNECT':
                    name = self.getNameByAddr(addr)
                    clients.remove((name, addr))
                    msg1 = f'[SERVER] {name} disconnected from the server!\n'
                    msg2 = f'[SERVER] Now connected: {len(clients)} users'
                    message = msg1 + msg2
                    sock.sendto(message.encode(FORMAT), SERVER_ADDR)
                    continue

                result, old_name = self.isAdded(addr, name)
                if result == 2:
                    message = f'[SERVER] {old_name} changed his nickname to {name}!'
                    sock.sendto(message.encode(FORMAT), SERVER_ADDR)
                    sock.sendto('1'.encode(FORMAT), addr)   # Saying to the client that the name changed
                    continue
                elif result:
                    continue
                else:
                    new_client = ClientsData(name, addr)
                    clients.add(new_client.getData())
                    sock.sendto('1'.encode(FORMAT), addr)    # Saying to the client that he's connected
                    msg1 = f'[SERVER] {name} connected to the server!\n'
                    msg2 = f'[SERVER] Now connected: {len(clients)} users'
                    message = msg1 + msg2
                    sock.sendto(message.encode(FORMAT), SERVER_ADDR)
            except:
                time.sleep(1)

    def isAdded(self, addr, name=None, sock=None):
        clients = self.getClients()
        for client in clients:
            if client[1] == addr:
                if name != None and client[0] != name:  # This method also do the name change 
                    new_client = list(client)           # 'cos it's faster that way
                    new_client[0] = name
                    new_client = tuple(new_client)
                    clients.remove(client)
                    clients.add(new_client)
                    return 2, client[0]
                return True, 0
        return False, 0

    def getClients(self):
        return self._clients

    def getNameByAddr(self, addr):
        for client in self.getClients():
            if client[1] == addr:
                return client[0]
        return '!NAME_ERROR'


class Messenger:
    def __init__(self):
        pass

    def loop(self, tk, sock, List):
        try:
            message, addr = sock.recvfrom(1024)
            message = message.decode(FORMAT)
            clients = List.getClients()
            
            nickname = List.getNameByAddr(addr)

            if nickname == 'Sett-0':
                message = bytes(nickname + ': ' + '*Silent wishper*', FORMAT)
            elif addr == CONN_ADDR:
                message = bytes(message, FORMAT)
            elif message == '':
                tk.after(10, self.loop, tk, sock, List)
            else:
                message = bytes(nickname + ': ' + message, FORMAT)

            for client in clients:
                sock.sendto(message, client[1])
            
            tk.after(10, self.loop, tk, sock, List)
        except:
            tk.after(10, self.loop, tk, sock, List)


if __name__ == '__main__':
    server = Server()
    server.RunSocket()
    connections = Connections()
    connections.RunSocket()
    window = ServerWindow()

    tk = window.getTK()
    servSock = server.getSocket()
    servPort = server.getPort()
    connSock = connections.getSocket()
    connPort = connections.getPort()

    m = Messenger()
    List = ClientsList()

    thread = threading.Thread(target=List.recvClients, args=(connSock,))
    thread.start()

    tk.after(1, m.loop, tk, servSock, List)
    tk.mainloop()
    thread.do_run = False
