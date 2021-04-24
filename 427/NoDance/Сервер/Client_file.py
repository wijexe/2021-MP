import time as ti

# --- Код,отвечающий за работу над клиентами,начинается здесь
class Clients:
    def __init__(self):
        self.path=r"C:\Users\emgam\Desktop\temp\Сервер\Cl_list.txt"
        self.bl_path=r"C:\Users\emgam\Desktop\temp\Сервер\BL_list.txt"
        self.fil_path=r"C:\Users\emgam\Desktop\temp\Сервер\Fltr.txt"
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
# -- Делал Куклев Даниил
# --- Код,отвечающий за работу над клиентами,заканчивается здесь