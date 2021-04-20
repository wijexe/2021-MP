import socket
from tkinter import *

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 50050
FORMAT = 'utf-8'
TITLE = 'Server'
SIZE = '400x300'

class Server:    
    _ip = ''
    _port = 0
    _sock = 0

    def __init__(self, ip=SERVER_IP, port=PORT):
        self._ip = ip
        self._port = port

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


class ServerWindow:
    _size = ''
    _title = ''
    _tk = 0

    def __init__(self, title=TITLE, size=SIZE):
        self._tk = Tk()
        self._tk.title(title)
        self._tk.geometry(size)
        
    def getTK(self):
        return self._tk

class Messenger:
    def __init__(self):
        pass

    def loop(self, tk, sock):
        try:
            message, addr = sock.recvfrom(1024)
            print(message.decode(FORMAT))

            if message.startswith('Sett-0'.encode(FORMAT)): 
                message = bytes('*Silent wishper*', FORMAT)
            
            sock.sendto(message, addr)
            print('message sent!')
            tk.after(10, self.loop, tk, sock)
        except:
            tk.after(10, self.loop, tk, sock)


if __name__ == '__main__':
    server = Server()
    server.RunSocket()
    window = ServerWindow()

    tk = window.getTK()
    sock = server.getSocket()
    port = server.getPort()
    m = Messenger()

    tk.after(10, m.loop, tk, sock)
    tk.mainloop()
