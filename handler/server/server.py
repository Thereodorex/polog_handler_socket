import socket
import time
import socketserver
import threading
import dateutil.parser
import json

# from queue import Queue
from config import HOST, PORT, START_MESSAGE, END_MESSAGE

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

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # smes = '"\\' + START_MESSAGE
        # emes = END_MESSAGE[:-1] + '\\""'
        data = self.request.recv(1024 * 1024)
        message = data
        message = data.decode()
        print(message)
        if message.startswith(START_MESSAGE) and message.endswith(END_MESSAGE):
            message = message[len(START_MESSAGE):-len(END_MESSAGE)]
            self.server.queue.add(message)
            self.request.send("Ok".encode())
        # if message.startswith(smes) and message.endswith(emes):
        #     message = message.split('_>')[1].split('</')[0]
        else:
            self.request.send("Invalid or very long message".encode())

class Queue:

    def __init__(self, ip, port):
        self.server = ThreadedTCPServer((ip, port), ThreadedTCPRequestHandler)
        self.server.queue = self
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

        self.messages = []

    def start_server(self):
        self.server_thread.start()
        print("Server loop running in thread:", self.server_thread.name)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()

    def add(self, message):
        self.messages.append(message)

    def view(self):
        return self.messages

    def get(self):
        return self.messages.pop()

    def exists(self):
        return len(self.messages)

class Server:

    def __init__(self, ip, port, handler=None):
        self.queue = Queue(ip, port)
        self.handler = handler

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
            if self.handler:
                args, kkw = json.loads(message)
                # kkw = args[1]
                # for k,v in kkw.items():
                #     if (len(v) == 2 and v[0] == 'datetime'):
                #         kkw[k] = dateutil.parser.parse(v[1])
                self.handler(args, **kkw)
            else:
                print(f"Got: {message}")
        except Exception as e:
            print(f"Error: {e}")

# if __name__ == "__main__":

#     print("Server started.")
#     app = Server(HOST, PORT)
#     app.start_server()
#     app.loop()
#     app.stop_server()