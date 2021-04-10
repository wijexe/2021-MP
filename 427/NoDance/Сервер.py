from socket import *  
import numpy as np
import time as ti
from threading import Thread
    
# Сервер
class Server():
        def __init__(self): # Установка сервера
            # Объвляем перменные класса 
            self.host=''; self.port=3000; self.b_size=1024 
            self.client=[] ; self.nick=[]; self.a=True ; self.i=0
            self.sockaddr=(self.host,self.port)
            self.server=socket(AF_INET,SOCK_DGRAM)
            self.server.bind(self.sockaddr)
            self.path=r"C:\Users\user\Documents\GitHub\NoDance1\Logs.txt"
            self.path1=r"C:\Users\user\Documents\GitHub\NoDance1\Clients.txt"
            self.file_open=open(self.path,'a')
            self.filter=[] ; self.BL=[]
            #self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
        def ServerStart(self): # Запуск сервера
            # Переменные для работы сервера
            serv=self.server ; clients=self.client ; size= self.b_size
            nicks= self.nick ; nick="" ; file=self.file_open
            Read=Support() # Класс поддержки
            path=r"C:\Users\user\Documents\GitHub\NoDance1\fltr.txt"
            filters,cnt=Read.ReadFilters(path) # Читаем фильтры
            self.BL=Read.WatchBlackList(self.path1)
            time= ti.ctime(ti.time()) ; msg=str(time)+"\n\n------------------------------------------------\n\n<Сервер запущен.>\n"
            print("Сервер запущен.\n\n") ; file.write(msg)
            while self.a==True:
                print("Waiting...")
                data,addr=serv.recvfrom(size) # Принимает сообщение от пользователей определенного размера
                d_data=data.decode('utf-8') # Расшифровка сообщения
                if addr not in clients: # Если клиента нет в списке клиентов
                    if d_data.startswith('n_'): # Если это сообщение с ником
                        k=2 ; n_data=""
                        while k<len(d_data): # Вытаскиваем из сообщения ник и записываем его 
                            n_data+= d_data[k]
                            k+=1
                        if n_data in self.BL:
                            msg="You shall not pass!"
                            print(n_data,' Пытался присоедениться,но он находится в чёрном списке')
                            serv.sendto(msg, addr)
                        else:
                            nicks.append(n_data) ; clients.append(addr) # Записываем ники и адреса в список
                            file1=open(self.path1,'r') ; n_list=[]
                            for line in file1:
                                n_list.append(line.replace('\n',''))
                            file1.close()
                            if n_data in n_list:
                                print(n_data," уже есть в списке")
                            else:
                                Read.AddClient(n_data)
                        
                            w_data="Привет, "+n_data+" !\nЕсли захочешь сменить ник - введи команду /Client.SwitchNick \"Ник\" (С пробелом)"
                            time= ti.ctime(ti.time())
                            tmp_data=str(time)+" "+str(addr)+" ["+nicks[self.i]+'] присоединился.\n'
                            print(str(time)," ",str(addr)," [",nicks[self.i],'] присоединился.') ; file.write(tmp_data) ; self.i+=1
                            serv.sendto(w_data.encode('utf-8'),addr) # Отправляем приыетсвтие новому пользователю
                            for j in range(len(clients)): # Отправка сообщения остальным клиентам
                                if clients[j] == addr:  continue # Отправившему сообщение не отправлять
                                else:
                                    time= ti.ctime(ti.time())
                                    s_data= str(time)+" ["+str(nicks[self.i-1])+"] присоединился к серверу."
                                    serv.sendto(s_data.encode('utf-8'),clients[j])
                else: # Если клиент уже есть в списке
                    if d_data.startswith('sn_'): # Меняем ник пользователя,если он это сделал
                        for k in range(len(clients)):
                            if addr == clients[k]: # Нашли пользователя,который сменил ник
                                l=3 ; tmp="" ; n_data
                                while l<len(d_data):
                                    tmp+=d_data[l]
                                    l+=1
                                print(tmp)
                                nck_data=tmp ; time= ti.ctime(ti.time()) ; n_data=nicks[k]
                                msg=str(time)+" "+str(addr)+" Сменил ник ["+nicks[k]+"] на ["+nck_data+"].\n"
                                print(time," ",addr," Сменил ник [",nicks[k],"] на [",nck_data,"]")
                                file.write(msg) ; nicks[k]=nck_data
                                s_data=str(time)+" Вы сменили ник на "+nck_data+"!"
                                serv.sendto(s_data.encode('utf-8'),addr)
                                for h in range(len(clients)):
                                    if clients[h]!=addr:
                                        s_data=str(time)+" Пользователь с ником ["+n_data+"] сменил свой ник на ["+str(nck_data)+"]."
                                        serv.sendto(s_data.encode('utf-8'),clients[h])
                    elif d_data.endswith('qqq'): # Удаляем пользователя,если он вышел
                        clients.remove(addr) ; self.i-=1 # Выводим сообщение об отсоединении клиента
                        time= ti.ctime(ti.time())
                        msg=str(time)+" "+str(addr)+" отсоединился.\n"
                        print(time," ",addr," отсоединился.")
                        file.write(msg)
                        
                        continue
                    else: # Отсылаем присланное одним пользователем сообщение остальным
                        time= ti.ctime(ti.time())
                        for j in range(len(clients)):
                            if clients[j] == addr: 
                                nick=nicks[j]
                                msg=str(time)+" "+str(addr)+" ["+nick+"] "+d_data+"\n"
                                print(time," ",addr," [",nick,"] ",d_data)
                                file.write(msg) # Записываем в лог сообщение
                        for j in range(len(clients)): # Отправляем всем сообщение
                            if clients[j] != addr: 
                                time= ti.ctime(ti.time())
                                for i in range(cnt):
                                    if filters[i] in d_data:
                                        print('Processing...')
                                        d_data=d_data.replace(filters[i],'*******')
                                s_data= str(time)+" ["+nick+"]: "+ d_data
                                serv.sendto(s_data.encode('utf-8'),clients[j])
                ti.sleep(0.001) # Задержка в отправке
            serv.close() ; file.close()
        def ServerCommands(self): # Команды сервера
            Read=Support()
            path=r"C:\Users\user\Documents\GitHub\NoDance1\fltr.txt"
            filters,cnt=Read.ReadFilters(path)
            print("\n\n-----\n\n") ; print("Чтобы выключить сервер,введите команту </Server.Quit> (Без галок)\n")
            print("Чтобы очистить лог,введите команду </Server.ClearLog> (Без галок)\n") 
            print("Чтобы выключить сервер и удалить лог,введите команду </Server.QuitWithoutLog> (Без галок)\n")
            print("Всего фильтров: ",cnt, "\nЧтобы посмотреть все фильры,введите команду </Server.ShowFilters> (Без галок)")
            print("--Чтобы добавить фильтр,введите команду </Server.AddFilter \'Фильтр\'> (Без галок и кавычек)")
            print("--Чтобы убрать фильтр,введите команду </Server.RemoveFilter \'Фильтр\'> (Без галок и кавычек)\n")
            print("Чтобы удалить пользователя,введите команду </Server.BanClient \'Имя клиента\'> (Без галок и кавыычек)")
            print("\n\n-----\n\n") ; command=input()
            while self.a==True:
                if command.startswith('/Server.Quit'):
                    time= ti.ctime(ti.time()) ; msg= "\n<Сервер закончил свою работу>\n\n------------------------------------------------"
                    s_data="*_"+str(time)+" <Сервер закончил свою работу>\n"
                    print("Сервер закончил работу.\nПожалуйста,закройте окно.")
                    for j in range(len(self.client)):
                        self.server.sendto(s_data.encode('utf-8'),self.client[j])
                    self.file_open.write(msg) ; self.file_open.close() ; self.a=False
                    break
                elif command.startswith('/Server.ClearLog'):
                    self.file_open.close() ; self.file_open= open(self.path,'w')
                    self.file_open.write('\n') ; self.file_open.close() ; self.file_open= open(self.path,'a')
                    print("Лог очищен.")
                elif command.startswith('/Server.QuitWithoutLog'): # Завершение работы сервера с очисткой лога
                    time= ti.ctime(ti.time())
                    s_data="*_"+str(time)+" <Сервер закончил свою работу>\n"
                    for j in range(len(self.client)):
                        self.server.sendto(s_data.encode('utf-8'),self.client[j])
                    self.file_open.write(s_data) ; self.file_open.close() ; self.a=False
                    self.file_open.close() ; self.file_open= open(self.path,'w')
                    self.file_open.write('\n') ; self.file_open.close()
                    print("Сервер закончил работу и лог очищен.\nПожалуйста,закройте окно.")
                    break
                elif command.startswith('/Server.ShowFilters'):
                    print("Список фильтров:")
                    filters,cnt=Read.ReadFilters(path)
                    for i in range(cnt):
                        print('-',filters[i])
                elif command.startswith('/Server.AddFilter'):
                    self.filter=filters=Read.AddFilters(path,command,filters,cnt)
                elif command.startswith('/Server.RemoveFilter'):
                    self.filter=filters=Read.RemoveFilter(path, command, filters, cnt)
                elif command.startswith('/Server.BanClient'):
                    self.client,self.nick,self.i = Read.BanClient(self.path1, self.client, self.nick,command, self.i)
                else:
                    print("Нет такой команды: ",command)
                command="" ; command=input()

#Класс поддержки
class Support():
    
    def ReadFilters(self,path): # Записывает фильтры в список и закрывает файл
        file=open(path,'r') ; filters=[] ; fltr_count=0 ; tmp=""
        for line in file:
                for j in range(len(line)):
                    if j<len(line)-1:
                        tmp+=line[j]
                filters.append(tmp)
                tmp="" ; fltr_count+=1
        file.close() ; arr=[filters,fltr_count]
        return arr
    
    def AddFilters(self,path,cmd,arr,cnt): # Добавляет новый фильтр в конец списка
        fltr=open(path,'a')
        n_fltr=""
        for i in range(len(cmd)):
            if i> 17:
                if cmd[18]=="":
                    print('Не был введён фильтр на добавление.')
                    break
                else:
                    n_fltr+=cmd[i]
        if cmd[18]!="":
            cnt+=1 ; n_fltr+='\n'
            fltr.write(n_fltr) ; fltr.close() ; print("Фильтр добавлен.")
        return arr
    
    def RemoveFilter(self,path,cmd,arr,cnt): # Переписывает список фильтров
        fltr=open(path,'r') ; lines=fltr.readlines() ; fltr.close()
        tmp="" ; fltr_n="" ; fltrs=[]
        for i in range(len(cmd)):
            if i>20:
                if cmd[21]=="":
                    print('Не был введёт фильтр на удаление.')
                    break
                fltr_n+=cmd[i]
        if cmd[21]!="":
            for line in lines:
                for j in range(len(line)):
                    if j<len(line)-1:
                        tmp+=line[j]
                fltrs.append(tmp) ; tmp=""
            fltr=open(path,'w')
            for i in range(len(fltrs)):
                if fltrs[i]!=fltr_n:
                    if i<len(fltrs)-1:
                        fltrs[i]+='\n' ; fltr.write(fltrs[i])
                    else: 
                        fltrs[i]+=' ' ; fltr.write(fltrs[i])
            fltr.close() ; cnt-=1 ; print("Фильтр удалён.")
        return arr
    
    def AddClient(self,nick):
        path=r"C:\Users\user\Documents\GitHub\NoDance1\Clients.txt"
        nick="\n"+nick
        file=open(path,'a') ; file.write(nick)
        file.close()
        
    def BanClient(self,path,cl_list,ncks,cmd,cnt):
        path = r"C:\Users\user\Documents\GitHub\NoDance1\Clients.txt"
        path1= r"C:\Users\user\Documents\GitHub\NoDance1\BlackList.txt"
        file = open(path,'r') ;  n_list =[] ; n_list1=[] ; tmp=''
        for line in file:
            n_list.append(line.replace('\n',''))
        file.close()
        i=17 ; nick=""
        for i in range(len(cmd)):
            if i >17:
                nick+=cmd[i]
        for i in range(len(ncks)):
            if nick ==ncks[i]:
                ncks.remove(ncks[i])
                cl_list.remove(cl_list[i])
        tmp= nick+'\n'
        for i in range(len(n_list)):
            if nick!=n_list[i]:
                n_list1.append(n_list[i])
            else: continue
        file = open(path,'w')
        for i in range(len(n_list1)):
            n_list1[i]=n_list1[i]+'\n'
            file.write(n_list1[i])
        file.close()
        file=open(path1,'a')
        file.write(tmp) ; file.close() ; cnt-=1
        print('Пользователь добавлен в Чёрный список сервер.')
        arr=cl_list,n_list,cnt
        return arr
    
    def WatchBlackList(self,path):
        file=open(path,'r') ; black_l=[]
        for line in file:
            black_l.append(line.replace('\n',''))
        return black_l
        
a=Server() # Объявляем сервер и в два потока записываем команды
Thread(target=a.ServerStart).start()
Thread(target=a.ServerCommands).start()