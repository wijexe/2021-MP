import socket
import threading

server = socket.socket(

    socket.AF_INET,
    socket.SOCK_STREAM,

    )

server.bind(
    ('127.0.0.1', 1234)
    )

server.listen(5)

print('server is listening')

users = []

def send_all(data):
    
    for user in users:
        
        user.send(data)

        
def listen_user(user):
    while True:
        
        data = user.recv(2048)
        
        print(f'пользователь отправил {data}')
        
        send_all(data)

def start_server():
  
    

    while True:
        
        user_socket, address = server.accept()
        
        print(f' user <{address[0]}> connected!')

        users.append(user_socket)
        
        listen_accepted_user = threading.Thread(
            target=listen_user,
            args=(user_socket, ))
        
        listen_accepted_user.start()
        
        

       
        

  

if __name__ == '__main__':

    
    start_server()

    

    
    
