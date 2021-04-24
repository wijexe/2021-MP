class Support:
    def PullOutContent(self,data,cnt):
        i=cnt ; tmp=''
        while i<len(data):
            tmp+=data[i] ; i+=1
        return tmp
    
    def SetUpNick(self): return input('Введите ник: ')
    def EnterData(self): return input()