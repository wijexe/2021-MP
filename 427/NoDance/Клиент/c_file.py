from socket import *

class ClientConnection:
    def StartWorking(self):
        self.host='127.0.0.1' ; self.port=3000 ; self.b_size=1024
        self.sockaddr=(self.host,self.port) ; self.client=socket(AF_INET,SOCK_DGRAM)
        
    def StopWorking(self,a):
        a=False ; self.client.close() ; return a
        
    def ReceiveMsg(self):
        data,addr=self.client.recvfrom(self.b_size)
        d_data=data.decode('utf-8') ; arr=d_data,addr
        return arr
    
    def SendMsg(self,data): self.client.sendto(data.encode('utf-8'), self.sockaddr)
        
    def SendEnteringMsg(self,data): s_data='n_'+data ; self.client.sendto(s_data.encode('utf-8'),self.sockaddr)
        
    def SendChanginNickMsg(self,data): s_data='sn_'+data ; self.client.sendto(s_data.encode('utf-8'),self.sockaddr)
        
    def SendLeavingMsg(self,data): s_data='lv_'+data ; self.client.sendto(s_data.encode('utf-8'),self.sockaddr)
        
    def ChangingNickMsg(self,data): s_data='sn_'+data ; self.client.sendto(s_data.encode('utf-8'),self.sockaddr)