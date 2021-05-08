import socket
import time

host = socket.gethostbyname(socket.gethostname()) #можно попробовать потом = '192.168.0.101'
port = 9090

clients = [] # список клиентов, принимает адреса, а не username

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # создаём сокет, обьявляет протоколы tcp и udp в переменную s
s.bind((host,port))

quit = False
print('Сервер запущен!')

while not quit:
    try:
        data, addr = s.recvfrom(1024)

        if addr not in clients:
            clients.append(addr)
        
        itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()) # отображает время сообщения

        print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/", end="")
        print(data.decode("utf-8")) # декодируем наше сообщение

        for client in clients: # проверка, чтобы клиенту не отправилось его же сообщение
            if addr != client:
                s.sendto(data,client)
    except:
        print("\n Сервер остановлен!")
        quit = True

s.close()
