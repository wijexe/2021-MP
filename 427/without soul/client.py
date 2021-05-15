mport socket
import time
import threading

key = 8194 # ключ для шифровки данных (# Begin - #end)

shutdown = False
join = False

# Принятие сообщений от другого пользователя
def receving (name, sock): # name == self
    while not shutdown:
        try: # try - проверяется на наличие ошибок; если ошибка есть, то except -> pass - пропускаем
            while True:
                data, addr = sock.recvfrom(1024)

                # Шифровка данных (сообщение шифруется для сервера, а потом сервер его расшифровывает получателю)
                # Begin
                decpypt = ""; k = False
                for i in data.decode("utf-8"):
                    if i == ":":
                        k = True
                        decpypt += i
                    elif k == False or i == " ":
                        decpypt += i
                    else:
                        decpypt += chr(ord(i)*key)
                print(decpypt)
                # End
                
                time.sleep(0.2)
        except:
            pass

host = socket.gethostbyname(socket.gethostname())
port = 0 # порт равен 0, так как наш клиент лишь подключается к сети, а не создаёт её

server = ("192.168.0.101", 9090) # указываем локал-хост и порт нашего сервера

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # создаём tcp и ip соединение
s.bind((host, port)) # присваиваем клиенту его идентификацию, то есть наделяем его ip и портом
s.setblocking(0)

alias = input("Name: ")

# Запускаем многопоточность
rT = threading.Thread(target= receving, args= ("RecvThread", s))
rT.start()

# Отправка сообщения
while shutdown ==  False: # пока клиент не вышел
    if join == False: # если пользователь не присоединён
        s.send(("["+alias + "] => join chat ").encode("utf-8"),server) # отправляем сообщение серверу, что он вошёл
        join = True
    else:
        try:
            message = input() # даём способность отправляеть неогр. кол-во сообщений
            
            # Криптографическая связь (зашифровываем наше сообщение)
            # Begin 
            crypt = ""
            for i in message:
                crypt += chr(ord(i)*key)
            message = crypt
            # End

            if message != "" :
                s.sendto(("["+alias + "] :: "+message).encode("utf-8"), server) # сообщение отправителя (alias) кодируется и передаётся серверу и пересылается пользователяем
            
            time.sleep(0.2)
        except:
            s.sendto(("["+alias + "] <= left chat ").encode("utf-8"), server) # если произошла ошибка (например: клиент закрыл чат), то серверу отправляется информация, что клиент вышел из чата
            shutdown = True

rT.join()
s.close()
