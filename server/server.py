import socket
import time

from queue import Queue
from config import HOST, PORT

# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024).decode()
#             print(data)
#             response = "Ok"
#             if not data:
#                 response = "NotOk"
#                 break
#             conn.send(response.encode())



class Server:

    def __init__(self, ip, port):
        self.queue = Queue(ip, port)

    def start_server(self):
        self.queue.start_server()

    def stop_server(self):
        self.queue.stop_server()

    def loop(self):
        while True:
            if self.queue.exists():
                self.handle(self.queue.get())

    def send(self, ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        try:
            sock.sendall(message.encode())
        finally:
            sock.close()

    def handle(self, message):
        try:
            print(f"Got: {message.decode()}")
        except Exception as e:
            print(f"Error: {message.decode()}")

if __name__ == "__main__":

    print("Server started.")
    app = Server(HOST, PORT)
    app.start_server()
    app.loop()
    app.stop_server()