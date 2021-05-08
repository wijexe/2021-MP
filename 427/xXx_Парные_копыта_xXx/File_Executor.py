import time

class FileExecutor():
    def writeDown_name(self, name):
        f = open('name.txt', 'a')
        f.write(name + '\n')
        f.close()
    def writeDown_log(self, data):
        f = open('logs.txt', 'a')
        f.write(str(time.time()) + ' ' + data + '\n')
        f.close()
