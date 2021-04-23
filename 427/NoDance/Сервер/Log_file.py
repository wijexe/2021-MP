import time as ti

# --- Код,отвечающий за работу с логами,начинается здесь
class ServerLogs:
    def __init__(self):
        self.log_path=r'C:\Users\emgam\Desktop\temp\Сервер\Logs.txt' ; file=open(self.log_path,'a')
        self.client_path=r"C:\Users\emgam\Desktop\temp\Сервер\Cl_list.txt"
        start='\n------------------------------\nTime: '+ti.ctime(ti.time())+'\n' ; file.write(start) ; file.close()
    
    def LogConnectedClient(self,addr,n_data):
        file=open(self.log_path,'a') ; s_data='\n- '+str(addr)+' - ['+n_data+'] присоединился к серверу.' ; file.write(s_data) ; file.close()
      
    def LogDisconnectedClient(self,addr):
        file=open(self.log_path,'a') ; s_data='\n- '+str(addr)+' отсоединился.' ; file.write(s_data) ; file.close()
        
    def LogAddedFilter(self,fltr):
        file=open(self.log_path,'a') ; s_data='\n-- Добавлен новый фильтр: '+fltr ; file.write(s_data) ; file.close()
        
    def LogRemovedFilter(self,fltr):
        file=open(self.log_path,'a') ; s_data='\n-- Удалён фильтр: '+fltr ; file.write(s_data) ; file.close()
        
    def LogAddedBLClient(self,nick):
        file=open(self.log_path,'a') ; s_data='\n-- Пользователь ['+nick+'] был добавлен в чёрный список.' ; file.write(s_data) ; file.close()
        
    def LogRemovedBLClient(self,nick):
        file=open(self.log_path,'a') ; s_data='\n-- Пользователь ['+nick+'] был удалён из чёрного списка.' ; file.write(s_data) ; file.close()
    
    def LogTriedToConnectBLClient(self,nick):
        file=open(self.log_path,'a')
        s_data='\n- Пользователь ['+nick+'] пытался присоединиться,но он находится в чёрном списке.'
        file.write(s_data) ; file.close()
        
    def LogWrittenMsg(self,addr,data):
        file=open(self.log_path,'a') ; s_data='\n'+str(addr)+' - '+data ; file.write(s_data) ; file.close()
        
    def LogSwitchedNick(self,old_nick,new_nick):
        file=open(self.log_path,'a') ; s_data='\n- Пользователь ['+old_nick+'] сменил ник на ['+new_nick+'].' ; file.write(s_data) ; file.close()
        
    def LogStartedServer(self):
        file=open(self.log_path,'a') ; s_data= '<Сервер начал свою работу.>' ; file.write(s_data) ; file.close()
        
    def LogStoppedServer(self):
        file=open(self.log_path,'a') ; s_data= '\n<Сервер закончил свою работу.>' ; file.write(s_data) ; file.close()
    
    def ClearClientsLog(self):
        file=open(self.client_path,'w') ; file.write('') ; file.close()
    
    def ClearServerLog(self):
        file=open(self.log_path,'w') ; file.write('') ; file.close()
# -- Делала Лариошкина Арина
# --- Код,отвечающий за работу с логами,заканчивается здесь