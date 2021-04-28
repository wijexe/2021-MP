from Socket import Socket
import threading


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        server.listen(5)

        print('server is listening')

        self.users = []

    def send_data(self, data):
        for user in self.users:
            user.send(data)

    def listen_socket(self, listened_socket=None):
        print("Listening user")

        while True:
            data = listened_socket.recv(2048)
            print(f"User sent {data}")

            self.send_data(data)

    def accept_sockets(self):
        while True:
            user_socket, address = self.accept()
            print(f"User <{address[0]}> connected!")

            self.users.append(user_socket)
            listen_accepted_user = threading.Thread(
                target=self.listen_socket,
                args=(user_socket,)
            )
            listen_accepted_user.start()


  
    


        

  

if __name__ == '__main__':

    server = Server()
    server.set_up()

    

    
    
