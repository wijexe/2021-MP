import socket
from tkinter import *
import random, time

SERVER_IP = '192.168.1.106'
SERVER_PORT = 50050
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
SERVER_CONN_ADDR = (SERVER_IP, SERVER_PORT-1)

CLIENT_IP = socket.gethostbyname(socket.gethostname())
CLIENT_PORT = random.randint(50051, 60000)
CLIENT_ADDR = (CLIENT_IP, CLIENT_PORT)

FORMAT = 'utf-8'
TITLE = 'Chat'
SIZE = '600x400'
DEFAULT_NICKNAME = 'Guest-' + str(random.randint(1, 100))

class Client:
    def __init__(self, ip=CLIENT_IP, port=CLIENT_PORT):
        self._ip = ip
        self._port = port

    def RunSocket(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.bind(self.getAddress())
            self._sock.setblocking(False)
            print('Socket runned')
            print(f'[CURRENT CLIENT ADDRESS] {self.getAddress()}')
        except:
            print('[ERROR] Socket startup error\n')
        
    def CloseSocket(self):
        self.getSocket().shutdown(socket.SHUT_RDWR)
        self.getSocket().close()
        print('Socket closed')

    def getSocket(self):
        return self._sock

    def setAddres(self, ip, port):       
        # !!! Позже перенести обработку исключений на конпки !!!
        if port == SERVER_PORT and ip == SERVER_IP:
            print('[ERROR] Client address cannot be equal to server address\n')
            pass

        self._ip = ip
        self._port = port
        self.CloseSocket()
        print('Restarting socket...')
        self.RunSocket()
    
    def setIP(self, ip):
        if self.getPort() == SERVER_PORT and ip == SERVER_IP:
            print('[ERROR] Client address cannot be equal to server address\n')
            pass

        self._ip = ip
        self.CloseSocket()
        print('Restarting socket...')
        self.RunSocket()

    def setPort(self, port):
        if port == SERVER_PORT and self.getIP() == SERVER_IP:
            print('[ERROR] Client address cannot be equal to server address\n')
            pass

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


class ConnectToServer:
    def __init__(self, addr=SERVER_CONN_ADDR):
        self._addr = addr

    def Connecting(self, sock, name):
        isConnected = False
        servAddr = self.getAddress()
        while not isConnected:
            try:
                sock.sendto(name.encode(FORMAT), servAddr)
                answer = sock.recv(1).decode(FORMAT)
                isConnected = bool(answer)
            except:
                time.sleep(1)
        print('Connected to server')
    
    def getAddress(self):
        return self._addr


class ClientWindow:
    def __init__(self, title=TITLE, size=SIZE, defaultName=DEFAULT_NICKNAME):
        self._tk = Tk()
        self._tk.title(title)
        self._tk.geometry(size)

        self._nickname = StringVar()
        self._nickname.set(defaultName)
        self._text = StringVar()
        self._text.set('')

        self._log = Text(self._tk)
        self._nick = Entry(self._tk, textvariable=self._nickname)
        self._msg = Entry(self._tk, textvariable=self._text)

        self._msg.pack(side='bottom', fill='x', expand='true')
        self._nick.pack(side='bottom', fill='x', expand='true')
        self._log.pack(side='top', fill='both', expand='true')

        self._msg.focus_set()
        
    def getTK(self):
        return self._tk

    def getLog(self):
        return self._log

    def getNickname(self):
        return self._nickname

    def getText(self):
        return self._text

    def getMessage(self):
        return self._msg


class Messenger:
    def __init__(self, nickname):
        self._nickname = nickname

    def loop(self, tk, log, sock):
        log.see(END)
        try:
            message = sock.recv(1024).decode(FORMAT)
            message += '\n'
            log.insert(END, message)
            tk.after(10, self.loop, tk, log, sock)
        except:
            tk.after(10, self.loop, tk, log, sock)

    def send(self, event, nickname, text, sock):
        old_nickname = self.getNickname()
        nickname = nickname.get()

        if nickname != old_nickname:
            print('Waiting for the nickname change...')
            isApproved = False
            while not isApproved:
                try:
                    sock.sendto(nickname.encode(FORMAT), SERVER_CONN_ADDR)
                    answer = sock.recv(1).decode(FORMAT)
                    isApproved = bool(answer)
                except:
                    time.sleep(1)
            print('Nickname changed')
            self.setNickname(nickname)

        message = '%s' % text.get()
        sock.sendto(message.encode(FORMAT), SERVER_ADDR)
        text.set('')

    def setNickname(self, nickname):
        self._nickname = nickname

    def getNickname(self):
        return self._nickname


if __name__ == '__main__':

    client = Client()
    client.RunSocket()
    nickname = input('Please enter your nickname: ')
    if nickname == '':
        nickname = DEFAULT_NICKNAME
    window = ClientWindow(defaultName=nickname)

    messenger = Messenger(nickname)
    msg = window.getMessage()
    nickname = window.getNickname()
    text = window.getText()
    sock = client.getSocket()
    msg.bind('<Return>', 
             lambda event: messenger.send(event, nickname, text, sock))

    connection = ConnectToServer()
    connection.Connecting(sock, nickname.get())

    tk = window.getTK()
    log = window.getLog()
    tk.after(1, messenger.loop, tk, log, sock)
    tk.mainloop()
    sock.sendto('!DISCONNECT'.encode(FORMAT), SERVER_CONN_ADDR)