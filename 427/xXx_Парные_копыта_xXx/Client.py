from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
import socket
from PyQt5.QtGui import QColor
import GUI
import random


class Client(QtWidgets.QMainWindow, GUI.Ui_MainWindow):
    def __init__(self, host, port):
        super(Client, self).__init__()
        self.host = host
        self.port = port
        self.setupUi(self)
        self.timer = QTimer()
        self.after = 0
        self.name = 'Guest' + str(random.randint(1000, 9999))

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def set_host(self, host):
        self.host = host

    def set_port(self, port):
        self.port = port

    def show_text(self, name, text, time):
        if name == self.name:
            self.textBrowser.setTextColor(QColor(255, 0, 0, 200))
        else:
            self.textBrowser.setTextColor(QColor(30, 30, 30, 210))
        if time > self.after:
            self.textBrowser.append(text)
            self.textBrowser.append('')
            self.after = time

    def send_message(self, client, server):
        if self.lineEdit.text():
            self.name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        if text == 'qqq':
            message = self.name + " live the chat!"
            client.sendto(message.encode('utf-8'), server)
            try:
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                self.close()
            except Exception:
                pass
            return
        client.sendto(('[' + self.name + ']' + ' ' + text).encode('utf-8'), server)
        self.textEdit.clear()

    def get_messages(self):
        with open('logs.txt', encoding='utf-8') as f:
            content = f.read().splitlines()
        for text in content:
            words = text.split(' ')
            time = float(words[0])
            name = words[1][1:-1]
            text = "".join(text.rsplit(words[0]))
            self.show_text(name, text, time)

    def change_addr(self):
        self.set_port(random.randint(6000, 10000))
        self.set_host(socket.gethostbyname(myHostName)) #написано для дальнейшей реализации
        self.textBrowser.setTextColor(QColor(180, 30, 30, 210))
        self.textBrowser.append("Ваш новый порт: " + str(self.get_port()))


    def runClient(self):
        pass
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.bind((self.get_host(), self.get_port()))
        server = (str(self.get_host()), 5000)
        self.pushButton.clicked.connect(lambda: self.send_message(client, server))
        self.pushButton_1.clicked.connect(self.change_addr)
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(500)
        self.show()


myHostName = socket.gethostname()
host = socket.gethostbyname(myHostName)
port = random.randint(6000, 10000)
app = QtWidgets.QApplication([])
window = Client(host, port)
window.runClient()
app.exec_()
