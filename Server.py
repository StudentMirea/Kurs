import socket
import sys
import threading


PORT = 9009


class ChatServer(threading.Thread):
    def __init__(self, port, host='localhost'):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = set()  # current connections
        self.users_lock = threading.Lock()
        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print('Bind failed %s' % socket.error)
            sys.exit()

        self.server.listen(10)

    def send_to_all(self,message):
        with self.users_lock:
            for c in self.users:
                try:
                  c.sendall(message.encode())
                except ConnectionResetError:
                    print("connection closed")
                    with self.users_lock:
                        self.users.remove(c)

    def client_name(self,conn):
        with self.users_lock:
            self.users.add(conn)
        print("got to name")
        name = conn.recv(1024).decode()
        if name == "{close}":
            with self.users_lock:
                self.users.remove(conn)
            conn.close()
        else:
           if name == " ":
               name = "Anonimous"
               new_user_annnouncement = ("New user has joined")
           else:
              print("correct name "+name)
              new_user_annnouncement = (name +" has joined")
           self.send_to_all(new_user_annnouncement)
           self.client_messg(conn,name)

    def client_messg(self,conn,name):
        while True:
            message = conn.recv(4096).decode()
            if message == "{close}":
                exit_message = (name+" has left the chat")
                self.send_to_all(exit_message)
                with self.users_lock:
                    self.users.remove(conn)
                conn.close()
                break
            message = (name + ": "+message)
            self.send_to_all(message)

    def handle_connection(self, conn, addr):
        print('Client connected with ' + addr[0] + ':' + str(addr[1]))
        self.client_name(conn)


    def run(self):
        print('Waiting for connections on port %s' % (self.port))
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle_connection, args=(conn, addr)).start()


if __name__ == '__main__':
    server = ChatServer(PORT)
    server.run()

