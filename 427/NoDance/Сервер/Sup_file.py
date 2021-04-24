# --- Код отвечающий за работу вспомогательных функций начинается здесь
class Support:
    def PullOutNick(self,data,cnt):
        i=cnt ; tmp=''
        while i<len(data):
            tmp+=data[i] ; i+=1
        return tmp
    
    def CountFilters(self,fil_path):
        file=open(fil_path,'r') ; cnt=0
        for line in file:
            if line=='': break
            else: cnt+=1
        file.close()
        return cnt
        
    def CountBLClients(self,bl_path):
        file=open(bl_path,'r') ; cnt=0
        for line in file:
            if line=='': break
            else: cnt+=1
        return cnt
            
    def ReadFilters(self,fil_path):
        file=open(fil_path,'r')
        for line in file: print('-',line.replace('\n',''))
            
    def CheckClientInBL(self,addr,black_l):
        if addr not in black_l: return False
        else: return True
        
    def CheckClientNickInBL(self,nick,black_l):
        for i in range(len(black_l)): bl_nicks=black_l[i][2]
        if nick not in bl_nicks: return False
        else: return True
        
    def ReadBL(self,bl_path):
        file=open(bl_path,'r')
        for line in file: print('-',line.replace('\n',''))
# -- Делала Кривина Лиза
# --- Код отвечающий за работу вспомогательных функций начинается здесь