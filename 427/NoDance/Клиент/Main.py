from socket import *
from threading import Thread
import time as ti
from c_file import ClientConnection
from s_file import Support

class Client:
    def __init__(self):
        self.connection=ClientConnection() ; self.support= Support()
        
        self.run=True
        self.connection.StartWorking()
        self.connection.SendEnteringMsg(self.support.SetUpNick())
        
    def LookChat(self):
        ti.sleep(0.001)
        while self.run==True:
            data,addr=self.connection.ReceiveMsg()
            if data.startswith('*_'):
                d_data=self.support.PullOutContent(data, 2) ; print(d_data) ; self.runself.connection.StopWorking(self.run)
            elif data.startswith('bl_'):
                d_data=self.support.PullOutContent(data, 3) ; print(d_data) ; self.runself.connection.StopWorking(self.run)
            elif data.startswith('bll_'):
                d_data=self.support.PullOutContent(data, 4) ; print(d_data) ; self.runself.connection.StopWorking(self.run)
            else: print(data)
        ti.sleep(0.001)
        
    def ChatAndCommands(self):
        print('Чтобы сменить ник,введите команду </Client.SwitchNick \'Ник\'> (Без ковычек и галок)')
        print('Чтобы выйти,введите команду </Client.Quit> (Без галок)\n')
        while self.run==True:
            data=self.support.EnterData()
            if data.startswith('/Client.SwitchNick'): 
                s_data=self.support.PullOutContent(data, 19) ; self.connection.SendChanginNickMsg(s_data)
            elif data.startswith('/Client.Quit'): 
                self.connection.SendLeavingMsg(data) ; self.run=self.connection.StopWorking(self.run)
            else: 
                self.connection.SendMsg(data)
            ti.sleep(0.001)
            
a=Client()
Thread(target=a.LookChat).start()
Thread(target=a.ChatAndCommands).start()