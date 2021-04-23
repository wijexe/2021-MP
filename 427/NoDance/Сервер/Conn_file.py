from socket import *
import time as ti

# --- Код,отвечающий за соединение сервера с клиентами,начинается зздесь
class ServerConnection:
    def ServerStartWorking(self):
        self.host='' ; self.port=3000 ; self.b_size=1024
        self.sockaddr=(self.host,self.port) ; self.server=socket(AF_INET,SOCK_DGRAM)
        self.server.bind(self.sockaddr) ; print('\n<Сервер начал свою работу.>\n')
        
    def ReceiveMsg(self):
        data,addr=self.server.recvfrom(self.b_size)
        d_data=data.decode('utf-8') ; arr=d_data,addr
        return arr
    
    def SendMsg(self,data,addr):
        self.server.sendto(data.encode('utf-8'), addr)
        
    def SendMsgToAll(self,data,addr,Addr,Ncks,Fltr):
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
                
    def SendMsgToAll_1(self,data,addr,Addr,o_nck,nck):
        for i in range(len(Addr)):
            if Addr[i] != addr:
                time= ti.ctime(ti.time())
                s_data=time+'Пользователь ['+o_nck+'] поменял свой ник на ['+nck+'] !'
                try:    self.server.sendto(s_data.encode('utf-8'),Addr[i])
                except: pass
                
    def SendMsgToAll_2(self,data,Addr):
        for i in range(len(Addr)):
            try:    self.server.sendto(data.encode('utf-8'),Addr[i])
            except: pass
                
    def SendWelcomeMsg(self,data,addr):
        w_data='Привет, '+data+'!'
        try:    self.server.sendto(w_data.encode('utf-8'),addr)
        except: pass
        
    def SendWelcomeMsg_1(self,data,addr):
        w_data='И снова привет, '+data+'!'
        try:    self.server.sendto(w_data.encode('utf-8'),addr)
        except: pass
        
    def SendConnectedMsg(self,data,addr,Addr,Ncks):
        for i in range(len(Addr)):
            if Addr[i]!=addr:
                time= ti.ctime(ti.time())
                s_data=time+' ['+data+'] присоединился к серверу.'
                try:    self.server.sendto(s_data.encode('utf-8'),Addr[i])
                except: pass
                
    def SendDisconnectedMsg(self,addr,Addr,Nick):
        for i in range(len(Addr)):
            if addr!=Addr[i]:
                time= ti.ctime(ti.time())
                s_data=time+' ['+Nick[i]+'] Покинул сервер.'
                try:    self.server.sendto(s_data.encode('utf-8'),Addr[i])
                except: pass
            
    def SendAddingToBLMsg(self,nick,Addr,Nick):
        s_data='bl_Вы были заблокированы на сервере.\nПожалуйста,закройте оккно.'
        for i in range(len(Nick)):
            if Nick[i]==nick: self.server.sendto(s_data.encode('utf-8'),Addr[i])
            
        
    def ServerStopWorking(self):
        print("\n<Сервер закончил свою работую\.>\n")
        self.server.close()
# -- Делал Макушев Евгений
# --- Код,отвечающий за соединение сервера с клиентами,заканчивается зздесь