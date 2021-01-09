import socket
import time
import socketserver
import threading
import json
import dateutil.parser


def default_handler(args, **kwargs):
    pass
    # print(args)
    # print(kwargs)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        message = data.decode()
        i = 0
        while not message.endswith("\r\n\r\n"):
            i += 1
            message += data.decode()
            if i == 10:
                self.request.send("Invalid or very long message".encode())
                return
        message = message[:-4]
        self.server.queue.add(message)
        self.request.send("Ok".encode())


class Queue:
    def __init__(self, ip, port):
        self.server = ThreadedTCPServer((ip, port), ThreadedTCPRequestHandler)
        self.server.queue = self
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

        self.messages = []

    def start_server(self):
        self.server_thread.start()
        # print("Server loop running in thread:", self.server_thread.name)

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
    def __init__(self, ip, port, handlers=[default_handler]):
        self.queue = Queue(ip, port)
        self.handlers = handlers

    def start(self):
        self.queue.start_server()
        self.loop()
        self.stop_server()

    def stop_server(self):
        self.queue.stop_server()

    def loop(self):
        while True:
            try:
                if self.queue.exists():
                    self.handle(self.queue.get())
            except:
                pass

    def send(self, ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        try:
            sock.sendall(message.encode())
        finally:
            sock.close()

    def handle(self, message):
        try:
            if self.handlers:
                args, kkw = json.loads(message)
                for k,v in kkw.items():
                    if (type(v) == list and len(v) == 2 and v[0] == 'datetime'):
                        kkw[k] = dateutil.parser.parse(v[1])
                for handler in self.handlers:
                    handler(args, **kkw)
            else:
                pass
                # print(f"Got: {message}")
        except KeyboardInterrupt:
            print('bye')
            self.stop_server()
            exit(0)
        except Exception as e:
            print(e)
            # print(f"Error: {e}")
