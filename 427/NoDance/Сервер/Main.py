from socket import *  
import numpy as np
import time as ti
from threading import Thread
from Conn_file import ServerConnection
from Client_file import Clients
from Log_file import ServerLogs
from Sup_file import Support

# --- Главный код сервера начинается здесь
class Server:
    def __init__(self):
        self.connection=ServerConnection() ; self.clients=Clients()
        self.support=Support() ; self.logs=ServerLogs()
        self.a=True
        
    def StartWorking(self):
        self.connection.ServerStartWorking() ; self.logs.LogStartedServer()
        while self.a==True:
            d_data,addr=self.connection.ReceiveMsg()
            if d_data.startswith('n_'):
                n_data=self.support.PullOutNick(d_data,2)
            if d_data.startswith('sn_'):
                n_data=self.support.PullOutNick(d_data, 3)
                
                
            if (addr not in self.clients.Addr) and (n_data not in self.clients.Nick):
                if self.support.CheckClientNickInBL(n_data, self.clients.black_l) == False:
                    if d_data.startswith('n_'):
                        self.clients.AddClient(addr,n_data)
                        self.connection.SendWelcomeMsg(n_data,addr)
                        self.connection.SendConnectedMsg(n_data,addr,self.clients.Addr,self.clients.Nick)
                        self.logs.LogConnectedClient(addr,n_data)
                else:
                    msg='bll_You Shall Not PASS!\nВаш ник заблокирован на этом сервере.\nПожалуйста,закройте окно.'
                    self.logs.LogTriedToConnectBLClient(n_data)
                    self.connection.SendMsg(msg, addr)
            else:
                if self.support.CheckClientNickInBL(n_data, self.clients.black_l) == False:
                    if d_data.startswith('n_'):
                        self.connection.SendWelcomeMsg_1(n_data, addr)
                        self.connection.SendConnectedMsg(n_data,addr,self.clients.Addr,self.clients.Nick)
                        self.logs.LogConnectedClient(addr,n_data)
                    elif d_data.startswith('sn_'):
                        old_nick=self.clients.ChangeNick(addr, n_data)
                        mssg='Ваш ник успешно изменён!' ; self.connection.SendMsg(mssg, addr)
                        msg='Пользователь ['+old_nick+'] поменял свой ник на ['+n_data+'] !' 
                        self.connection.SendMsgToAll_1(msg,addr,self.clients.Addr,old_nick,n_data)
                        self.logs.LogSwitchedNick(old_nick, n_data)
                    elif d_data.startswith('lv_'):
                        self.connection.SendDisconnectedMsg(addr, self.clients.Addr,self.clients.Nick)
                        self.clients.RemClient(addr)
                        self.logs.LogDisconnectedClient(addr)
                    else:
                        self.connection.SendMsgToAll(d_data, addr, self.clients.Addr, self.clients.Nick,self.clients.Filters)
                        self.logs.LogWrittenMsg(addr, d_data)
            ti.sleep(0.001)
                    
    def ServerCommands(self):
        cnt=self.support.CountFilters(self.clients.fil_path)
        cnt1=self.support.CountBLClients(self.clients.bl_path)
        print("\n\n-----\n\n")
        print("Чтобы выключить сервер,введите команту </Server.Quit> (Без галок)\n")
        print("Чтобы очистить лог,введите команду </Server.ClearLog> (Без галок)\n") 
        print("Чтобы выключить сервер и удалить лог,введите команду </Server.QuitWithoutLog> (Без галок)\n")
        print("-Всего фильтров: ",cnt, "\n-Чтобы посмотреть все фильры,введите команду </Server.ShowFilters> (Без галок)")
        print("--Чтобы добавить фильтр,введите команду </Server.AddFilter \'Фильтр\'> (Без галок и кавычек)")
        print("--Чтобы убрать фильтр,введите команду </Server.RemoveFilter \'Фильтр\'> (Без галок и кавычек)" )
        print("-Всего пользователей в чёрном списке: ",cnt1,"\n-Чтобы посмотреть чёрный список,введите команду </Server.ShowBL> (Без галок)")
        print("--Чтобы добавить пользователя в чёррный список,введите команду </Server.AddClientToBL \'Имя клиента\'> (Без галок)")
        print("--Чтобы убрать клиента из чёрного списка,введите команду </Server.RemoveClientFromBL \'Имя клиента\'> (Без галок)")
        print("\n\n-----\n\n")
        
        while self.a==True:
            command=input()
            if command.startswith('/Server.Quit'):
                time= ti.ctime(ti.time()) ; msg="*_"+str(time)+" <Сервер закончил свою работу>\n"
                self.a=False
                self.connection.ServerStopWorking() ; self.connection.SendMsgToAll_2(msg,self.clients.Addr)
                self.logs.LogStoppedServer() ; self.logs.ClearClientsLog()
            elif command.startswith('/Server.QuitWithoutLog'):
                time= ti.ctime(ti.time()) ; msg="*_"+str(time)+" <Сервер закончил свою работу>\n"
                self.connection.ServerStopWorking() ; self.connection.SendMsgToAll_2(msg,self.clients.Addr)
                self.logs.ClearServerLog() ; self.logs.ClearClientsLog() ; self.a=False
            elif command.startswith('/Server.ClearLog'):
                print('Логи очищены.') ; self.logs.ClearServerLog()
            elif command.startswith('/Server.ShowFilters'):
                self.support.ReadFilters(self.clients.fil_path)
            elif command.startswith('/Server.AddFilter'):
                fltr=self.support.PullOutNick(command, 18)
                self.clients.AddFilter(fltr) ; self.logs.LogAddedFilter(fltr)
            elif command.startswith('/Server.RemoveFilter'):
                fltr=self.support.PullOutNick(command, 21)
                self.clients.RemFilter(fltr) ; self.logs.LogRemovedFilter(fltr)
            elif command.startswith('/Server.ShowBL'):
                self.support.ReadBL(self.clients.bl_path)
            elif command.startswith('/Server.AddClientToBL'):
                nick=self.support.PullOutNick(command, 22)
                self.connection.SendAddingToBLMsg(nick, self.clients.Addr, self.clients.Nick)
                self.clients.AddBLClient(nick)
                self.logs.LogAddedBLClient(nick)
            elif command.startswith('/Server.RemoveClientFromBL'):
                nick=self.support.PullOutNick(command, 27)
                self.clients.RemBLClient(nick)
                self.logs.LogRemovedBLClient(nick)
            else: print('Нет такой команды: ',command)
            ti.sleep(0.001)
# --- Главный код сервера заканчивается здесь

a=Server()
Thread(target=a.StartWorking).start()
Thread(target=a.ServerCommands).start()