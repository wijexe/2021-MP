from socket import *  
import time as ti
from threading import Thread


# Сервер конект
class SerCon:
    def SerWork(self):
        self.host='' ; self.port=3000 ; self.b_size=1024
        self.sockaddr=(self.host,self.port) ; self.server=socket(AF_INET,SOCK_DGRAM)
        self.server.bind(self.sockaddr) ; print('\n<Кручу шестеренки и раздупляюсь.>\n')
        
    def polMsg(self):
        data,addr=self.server.recvfrom(self.b_size)
        d_data=data.decode('utf-8') ; arr=d_data,addr
        return arr
    
    def otprMsg(self,data,addr):
        self.server.sendto(data.encode('utf-8'), addr)
        
    def otprMsgvs(self,data,addr,Addr,Ncks,Fltr):
        for i in range(len(Addr)):
            if addr==Addr[i]: 
                nick=Ncks[i]
        for i in range(len(Addr)):
            if addr!=Addr[i]:
                time= ti.ctime(ti.time())
                for j in range(len(Fltr)): 
                    if Fltr[j] in data:
                        data=data.replace(Fltr[j],'*******')
                s_data=time+' ['+nick+'] - '+data
                try:    self.server.sendto(s_data.encode('utf-8'),Addr[i])
                except: pass
                
    def otprMsgvs1(self,data,addr,Addr,o_nck,nck):
        for i in range(len(Addr)):
            if Addr[i] != addr:
                time= ti.ctime(ti.time())
                s_data=time+'Пользователь ['+o_nck+'] изменил ник на ['+nck+'] !'
                try:    self.server.sendto(s_data.encode('utf-8'),Addr[i])
                except: pass
                
    def otprMsgvs2(self,data,Addr):
        for i in range(len(Addr)):
            try:    self.server.sendto(data.encode('utf-8'),Addr[i])
            except: pass
                
    def otprprivMsg(self,data,addr):
        w_data='Ку-Ку бро, теперь ты с нами, '+data+'!'
        try:    self.server.sendto(w_data.encode('utf-8'),addr)
        except: pass
        
    def otprprivMsg1(self,data,addr):
        w_data='Шалом, '+data+'!'
        try:    self.server.sendto(w_data.encode('utf-8'),addr)
        except: pass
        
    def otprConMsg(self,data,addr,Addr,Ncks):
        for i in range(len(Addr)):
            if Addr[i]!=addr:
                time= ti.ctime(ti.time())
                s_data=time+' ['+data+'] Заглянул на огонек.'
                try:    self.server.sendto(s_data.encode('utf-8'),Addr[i])
                except: pass
                
    def otprDisconMsg(self,addr,Addr,Nick):
        for i in range(len(Addr)):
            if addr!=Addr[i]:
                time= ti.ctime(ti.time())
                s_data=time+' ['+Nick[i]+'] Предал братство.'
                try:    self.server.sendto(s_data.encode('utf-8'),Addr[i])
                except: pass
            
    def otprvBanMsg(self,nick,Addr,Nick):
        s_data='bl_Вас исключили из тусовки.\nНа этом все!.'
        for i in range(len(Nick)):
            if Nick[i]==nick: self.server.sendto(s_data.encode('utf-8'),Addr[i])
            
        
    def SerStop(self):
        print("\n<Сервер пошел отдыхать.>\n")
        self.server.close()

#Супорт
class Sup:
    def PNick(self,data,cnt):
        i=cnt ; tmp=''
        while i<len(data):
            tmp+=data[i] ; i+=1
        return tmp
    
    def filt(self,fil_path):
        file=open(fil_path,'r') ; cnt=0
        for line in file:
            if line=='': break
            else: cnt+=1
        file.close()
        return cnt
        
    def BanClients(self,bl_path):
        file=open(bl_path,'r') ; cnt=0
        for line in file:
            if line=='': break
            else: cnt+=1
        return cnt
            
    def Rfilt(self,fil_path):
        file=open(fil_path,'r')
        for line in file: print('-',line.replace('\n',''))
            
    def CheckBan(self,addr,black_l):
        if addr not in black_l: return False
        else: return True
        
    def CheckBanNick(self,nick,black_l):
        if nick not in black_l: return False
        else: return True
        
    def RBan(self,bl_path):
        file=open(bl_path,'r')
        for line in file: print('-',line.replace('\n',''))


#Логи
class ServerLogs:
    def __init__(self):
        self.log_path=r'C:\Users\VerSus\Desktop\мп\log.txt' ; file=open(self.log_path,'a')
        self.client_path=r"C:\Users\VerSus\Desktop\мп\clist.txt"
        start='\n------------------------------\nTime: '+ti.ctime(ti.time())+'\n' ; file.write(start) ; file.close()
    
    def LogConnectedClient(self,addr,n_data):
        file=open(self.log_path,'a') ; s_data='\n- '+str(addr)+' - ['+n_data+'] зашел проверить нас.' ; file.write(s_data) ; file.close()
      
    def LogDisconnectedClient(self,addr):
        file=open(self.log_path,'a') ; s_data='\n- '+str(addr)+' покинул чат.' ; file.write(s_data) ; file.close()
        
    def LogAddedFilter(self,fltr):
        file=open(self.log_path,'a') ; s_data='\n-- Добавлен новый позывной: '+fltr ; file.write(s_data) ; file.close()
        
    def LogRemovedFilter(self,fltr):
        file=open(self.log_path,'a') ; s_data='\n-- Удалён позывной: '+fltr ; file.write(s_data) ; file.close()
        
    def LogAddedBLClient(self,nick):
        file=open(self.log_path,'a') ; s_data='\n-- Пользователь ['+nick+'] был выгнан с позором.' ; file.write(s_data) ; file.close()
        
    def LogRemovedBLClient(self,nick):
        file=open(self.log_path,'a') ; s_data='\n-- Пользователь ['+nick+'] был помилован.' ; file.write(s_data) ; file.close()
    
    def LogTriedToConnectBLClient(self,nick):
        file=open(self.log_path,'a')
        s_data='\n- Пользователь ['+nick+'] пытался заскочить,но он не достоин.'
        file.write(s_data) ; file.close()
        
    def LogWrittenMsg(self,addr,data):
        file=open(self.log_path,'a') ; s_data='\n'+str(addr)+' - '+data ; file.write(s_data) ; file.close()
        
    def LogSwitchedNick(self,old_nick,new_nick):
        file=open(self.log_path,'a') ; s_data='\n- Пользователь ['+old_nick+'] сменил ник на ['+new_nick+'].' ; file.write(s_data) ; file.close()
        
    def LogStartedServer(self):
        file=open(self.log_path,'a') ; s_data= '<Сервер застучал шестеренками.>' ; file.write(s_data) ; file.close()
        
    def LogStoppedServer(self):
        file=open(self.log_path,'a') ; s_data= '\n<Сервер устал и ушел баиньки.>' ; file.write(s_data) ; file.close()
    
    def ClearClientsLog(self):
        file=open(self.client_path,'w') ; file.write('') ; file.close()
    
    def ClearServerLog(self):
        file=open(self.log_path,'w') ; file.write('') ; file.close()

#Сервер главный
class Server:
    def __init__(self):
        self.connection=SerCon() ; self.clients=Clients()
        self.support=Sup() ; self.logs=ServerLogs()
        self.a=True
        
    def StartWorking(self):
        self.connection.SerWork() ; self.logs.LogStartedServer()
        while self.a==True:
            d_data,addr=self.connection.polMsg()
            if d_data.startswith('n_'):
                n_data=self.support.PNick(d_data,2)
            if d_data.startswith('sn_'):
                n_data=self.support.PNick(d_data, 3)
                
                
            if (addr not in self.clients.Addr) and (n_data not in self.clients.Nick):
                if self.support.CheckBanNick(n_data, self.clients.black_l) == False:
                    if d_data.startswith('n_'):
                        self.clients.AddClient(addr,n_data)
                        self.connection.otprprivMsg(n_data,addr)
                        self.connection.otprConMsg(n_data,addr,self.clients.Addr,self.clients.Nick)
                        self.logs.LogConnectedClient(addr,n_data)
                else:
                    msg='Вы предали братство.\nДавай до свидания.'
                    self.logs.LogTriedToConnectBLClient(n_data)
                    self.connection.otprMsg(msg, addr)
            else:
                if self.support.CheckBanNick(n_data, self.clients.black_l) == False:
                    if d_data.startswith('n_'):
                        self.connection.otprprivMsg1(n_data, addr)
                        self.connection.otprConMsg(n_data,addr,self.clients.Addr,self.clients.Nick)
                        self.logs.LogConnectedClient(addr,n_data)
                    elif d_data.startswith('sn_'):
                        old_nick=self.clients.ChangeNick(addr, n_data)
                        mssg='Вы изменили ник!' ; self.connection.otprMsg(mssg, addr)
                        msg='Пользователь ['+old_nick+'] изменил ник на ['+n_data+'] !' 
                        self.connection.otprMsgvs1(msg,addr,self.clients.Addr,old_nick,n_data)
                        self.logs.LogSwitchedNick(old_nick, n_data)
                    elif d_data.startswith('lv_'):
                        self.connection.otprDisconMsg(addr, self.clients.Addr,self.clients.Nick)
                        self.clients.RemClient(addr)
                        self.logs.LogDisconnectedClient(addr)
                    else:
                        self.connection.otprMsgvs(d_data, addr, self.clients.Addr, self.clients.Nick,self.clients.Filters)
                        self.logs.LogWrittenMsg(addr, d_data)
            ti.sleep(0.001)
                    
    def ServerCommands(self):
        cnt=self.support.filt(self.clients.fil_path)
        cnt1=self.support.BanClients(self.clients.bl_path)
        print("\n\n-----\n\n")
        print("Уходя не забeдь меня выключbть командой </Server.Quit> \n")
        print("Чтобы начать с чистого листа введи команду </Server.ClearLog> \n") 
        print("Чтобы выйти и забыть введи </Server.QuitWithoutLog> \n")
        print("-Всего фильтров: ",cnt, "\n-Посмотреть позывные,введите команду </Server.ShowFilters> ")
        print("--выбрать позывной, командой </Server.AddFilter \'Фильтр\'> ")
        print("--Убрать позывной,введите команду </Server.RemoveFilter \'Фильтр\'> " )
        print("-Всего пользователей в бане: ",cnt1,"\n-Чтобы посмотреть список недостойных,введите команду </Server.ShowBL> ")
        print("--Чтобы отправить тело в бан,введите команду </Server.AddClientToBL \'Имя клиента\'> ")
        print("--Чтобы понять и простить ,введите команду </Server.RemoveClientFromBL \'Имя клиента\'> ")
        print("\n\n-----\n\n")
        
        while self.a==True:
            command=input()
            if command.startswith('/Server.Quit'):
                time= ti.ctime(ti.time()) ; msg="*_"+str(time)+" <Сервер пошел отдыхать>\n"
                self.a=False
                self.connection.SerStop() ; self.connection.otprMsgvs2(msg,self.clients.Addr)
                self.logs.LogStoppedServer() ; self.logs.ClearClientsLog()
            elif command.startswith('/Server.QuitWithoutLog'):
                time= ti.ctime(ti.time()) ; msg="*_"+str(time)+" <Сервер пошел отдыхать>\n"
                self.connection.SerStop() ; self.connection.otprMsgvs2(msg,self.clients.Addr)
                self.logs.ClearServerLog() ; self.logs.ClearClientsLog() ; self.a=False
            elif command.startswith('/Server.ClearLog'):
                print('Логи очищены.') ; self.logs.ClearServerLog()
            elif command.startswith('/Server.ShowFilters'):
                self.support.Rfilt(self.clients.fil_path)
            elif command.startswith('/Server.AddFilter'):
                fltr=self.support.PNick(command, 18)
                self.clients.AddFilter(fltr) ; self.logs.LogAddedFilter(fltr)
            elif command.startswith('/Server.RemoveFilter'):
                fltr=self.support.PNick(command, 21)
                self.clients.RemFilter(fltr) ; self.logs.LogRemovedFilter(fltr)
            elif command.startswith('/Server.ShowBL'):
                self.support.RBan(self.clients.bl_path)
            elif command.startswith('/Server.AddClientToBL'):
                nick=self.support.PNick(command, 22)
                self.connection.otprvBanMsg(nick, self.clients.Addr, self.clients.Nick)
                self.clients.AddBLClient(nick)
                self.logs.LogAddedBLClient(nick)
            elif command.startswith('/Server.RemoveClientFromBL'):
                nick=self.support.PNick(command, 27)
                self.clients.RemBLClient(nick)
                self.logs.LogRemovedBLClient(nick)
            else: print('Я не знаю что делать, давай по новой: ',command)
            ti.sleep(0.001)

class Clients:
    def __init__(self):
        self.path=r"C:\Users\VerSus\Desktop\мп\clist.txt"
        self.bl_path=r"C:\Users\VerSus\Desktop\мп\blist.txt"
        self.fil_path=r"C:\Users\VerSus\Desktop\мп\filtr.txt"
        self.Addr=[] ; self.Nick=[] ; self.clients_l=[] 
        self.black_l=[] ; self.Filters=[]
        file=open(self.bl_path,'r') 
        file1=open(self.fil_path,'r')
        file2=open(self.path,'r')
        for line in file:
            if line=='': break
            bl_cl=line.split('\t')
            addr=bl_cl[0],int(bl_cl[1]),bl_cl[2].replace('\n','')
            self.black_l.append(addr)
        for line in file1:
            if line=='': break
            self.Filters.append(line.replace('\n',''))
        for line in file2:
            if line=='': break
            cl_line=line.split('\t') ; ar=cl_line[0],int(cl_line[1])
            self.Addr.append(ar) ; self.Nick.append(cl_line[2])
            arr=cl_line[0],cl_line[1],cl_line[2].replace('\n','')
            self.clients_l.append(arr)
        file.close() ; file1.close() ; file2.close()
        
    def AddClient(self,addr,nick):
        file=open(self.path,'a')
        add=addr[0],addr[1]
        self.Addr.append(add) ; self.Nick.append(nick)
        client= addr[0]+'\t'+str(addr[1])+"\t"+nick+'\n' ; arr=addr[0],addr[1],nick.replace('\n','')
        self.clients_l.append(arr) ; file.write(client)
        file.close()
        
    def RemClient(self,addr):
        file=open(self.path,'w')
        for i in range(len(self.Addr)):
            if self.Addr[i]==addr:
                tmp=self.Addr[i] ; tmp_n=self.Nick[i] ; tmp_cl=self.clients_l[i]
        self.Addr.remove(tmp) ; self.Nick.remove(tmp_n) ; self.clients_l.remove(tmp_cl)
        for i in range(len(self.Addr)):
            s=self.Addr[i][0]+'\t'+str(self.Addr[i][1])+'\t'+self.Nick[i] ; file.write(s)
        file.close()
        
    def AddFilter(self,fltr):
        if fltr=='':    pass
        else:
            file=open(self.fil_path,'a') ; self.Filters.append(fltr)
            s='\n'+fltr ; file.write(s) ; file.close()
        
    def RemFilter(self,fltr):
        file=open(self.fil_path,'w') ; self.Filters.remove(fltr)
        for i in range(len(self.Filters)):
            if i == len(self.Filters)-1:
                s=self.Filters[i]
                file.write(s)
            else:
                s=self.Filters[i]+'\n'
                file.write(s)
        file.close() 
        
    def AddBLClient(self,nick):
        file=open(self.bl_path,'a') ; self.black_l.append(nick)
        for i in range(len(self.Nick)):
            if self.Nick[i]==nick:
                addr=self.Addr[i]
                try:    self.Nick.remove(self.Nick[i]) ; self.Addr.remove(self.Addr[i])
                except: pass
        bl_client='\n'+addr[0]+'\t'+str(addr[1])+'\t'+nick
        file.write(bl_client) ; file.close()
        
    def RemBLClient(self,nick):
        file=open(self.bl_path,'w')
        print(self.black_l)
        for i in range(len(self.black_l)):
            if self.black_l[i][2]==nick:
                self.black_l.remove(self.black_l[i][2])
            else:
                s=self.black_l[0]+'\t'+str(self.black_l[1])+'\t'+self.black_l[2]+'\n'
                file.write(s)
        file.close()
        
    def ChangeNick(self,addr,new_nick):
        for i in range(len(self.Addr)):
            if str(self.Addr[i])==str(addr):
                old_nick=self.Nick[i]
                self.Nick[i]=new_nick
        file=open(self.path,'w')
        for i in range(len(self.Addr)):
            s=str(self.Addr[i])+'\t'+self.Nick[i]+'\n'
            file.write(s)
        file.close()
        return old_nick
    
a=Server()
Thread(target=a.StartWorking).start()
Thread(target=a.ServerCommands).start()


