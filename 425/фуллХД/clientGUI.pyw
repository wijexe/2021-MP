import socket # библиотека для обмена сокетами
import threading
import queue
import datetime
import sys # библиотека для работы с системными функциями
import random # библиотека для работы с рандомом
import os # библиотека для работы с операционной системой
from tkinter import *
from tkinter import messagebox as mb

name = ''
serverIP = ''
host = socket.gethostbyname(socket.gethostname())
port = random.randint(6000,10000)
connection_logic = False
data=''
k = 0

def clientStart():
	global data,name,serverIP,server
	server = (str(serverIP),5000)
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.bind((host,port))
	s.sendto(name.encode('utf-8'),server)
	threading.Thread(target=ReceiveData,args=(s,)).start()
	while True: # бесконечный цикл # информация - входная с клавиатуры
		if data == 'qqq': # Если информация = qqq, то завершаем цикл
			break
		elif data=='': # Если информация = пустой строке, то продолжаем цикл
			continue
		nowTime = datetime.datetime.today().strftime("%H:%M:%S")
		data = '('+nowTime+') ['+name+']' + ' -> '+ data # информация = [имя] -> информация
		s.sendto(data.encode('utf-8'),server) # отправляем информацию на сервер
		data = ''
	s.sendto(data.encode('utf-8'),server)# отправляем информацию на сервер при выходе(qqq)

def sendMessage(event):
	global data, chatText, k
	k+=1
	data = messageInput.get()
	nowTime = datetime.datetime.today().strftime("%H:%M:%S")
	mes = '('+nowTime+') ['+ name + '] -> ' + messageInput.get()
	print(mes)
	if k>13:
		chatText.delete("1.0","2.0")
		chatText.insert(END, mes+'\n')
	else:
		chatText.insert(END, mes+'\n')
	messageInput.delete(0, END)

def sendMessage2():
	global data, chatText, k
	k+=1
	data = messageInput.get()
	nowTime = datetime.datetime.today().strftime("%H:%M:%S")
	mes = '('+nowTime+') ['+ name + '] -> ' + messageInput.get()
	print(mes)
	if k>13:
		chatText.delete("1.0","2.0")
		chatText.insert(END, mes+'\n')
	else:
		chatText.insert(END, mes+'\n')
	messageInput.delete(0, END)

def ReceiveData(sock):
	global connectionButton, app, chatText, k
	while True:
		try:
			k+=1
			data,addr = sock.recvfrom(1024)
			mesIn = data.decode('utf-8')
			print(mesIn)
			if k>13:
				chatText.delete("1.0","2.0")
				chatText.insert(END, mesIn+'\n')
			else:
				chatText.insert(END, mesIn+'\n')
		except:
			pass

def openConnection():
	def chatConnect():
		global name,serverIP,connectionButton,app, connection_logic, clientStart, data
		if NameInput.get() == "":
			name = 'Guest'+str(random.randint(1000,9999))
			mb.showinfo("Внимание!","Ваше имя: "+str(name))
		else:
			name = NameInput.get()
		serverIP = ipInput.get()
		threading.Thread(target=clientStart).start()
		chat.destroy()
		chat.after(1000)
		connectionButton.config(text='Соединено', fg='green')

	global connectionButton
	chat = Toplevel()
	chat.geometry('300x300')
	chat.title('ФуллХД Чат')
	chat.wm_attributes('-alpha', 0.95)
	chat.resizable(width=False, height=False)
	canvasBackground = Canvas(chat, width=300, height=300)
	canvasBackground.pack()
	background_image = PhotoImage(file='ЧатКлиентConnection.png')
	canvasBackground.create_image(0,0,anchor=NW, image = background_image)
	canvasBackground.image=background_image
	
	textIP = Label(canvasBackground, text='Введите IP сервера:', bg='black', fg='white',font=40)
	textIP.place(relx=0.25, rely=0.35, relwidth=0.5, relheight=0.08)
	ipInput = Entry(canvasBackground, bg='white')
	ipInput.place(relx=0.1, rely=0.43, relwidth=0.8, relheight=0.08)

	textName = Label(canvasBackground, text='Введите ваше имя:', bg='black', fg='white',font=40)
	textName.place(relx=0.24, rely=0.57, relwidth=0.5, relheight=0.08)
	NameInput = Entry(canvasBackground, bg='white')
	NameInput.place(relx=0.1, rely=0.65, relwidth=0.8, relheight=0.08)

	conBut = Button(canvasBackground, text='Подключится', bg='black', fg='white', command=chatConnect)
	conBut.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.1)

app = Tk()
app['bg'] = '#689AD3'
app.title('ФуллХД Клиент')
app.wm_attributes('-alpha', 0.95)
app.geometry('800x600')
app.resizable(width=False, height=False)

app.iconphoto(True, PhotoImage(file='icon.png'))

canvasBG = Canvas(app, width=800, height=600)
canvasBG.pack()
bg_image = PhotoImage(file='ЧатКлиент.png')
canvasBG.create_image(0,0,anchor=NW, image = bg_image)

textIP = Label(canvasBG, text='Client IP -> '+str(host)+'\nPort -> '+str(port), bg='black', justify=LEFT, fg='white',font="TimesNewRoman 10").place(x=10,y=10)

messageInput = Entry(canvasBG, bg='white')
messageInput.place(relx=0.1, rely=0.85, relwidth=0.6, relheight=0.05)
messageInput.focus()
messageInput.bind('<Return>', sendMessage)
send_image = PhotoImage(file='Send.png')
Button(canvasBG, image=send_image, activebackground="black", bd=0, bg='black', command=sendMessage2).place(x=570,y=460)

chatText = Text(width=25, height=5, bg='black', fg='white', font=("Courier", 16), selectbackground='orange', insertbackground='orange', insertwidth=4, relief=RIDGE)
chatText.place(relx=0.1, rely=0.27, relwidth=0.8, relheight=0.51)

connectionButton = Button(canvasBG, text='Подключится \nк серверу', bg='black', activebackground="#FF8D24", bd=4, fg='white', command=openConnection)
connectionButton.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.07)

print(host,":",port, sep='')
app.mainloop()