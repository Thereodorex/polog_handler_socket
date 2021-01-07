from config import HOST, PORT
from handler.server.server import Server
from handler.client.socket_sender import Socket_Sender

def handler(args, **kwargs):
    print(args)
    print(kwargs)

def server_test():
    print("Server started.")
    app = Server(HOST, PORT, handler = handler)
    app.start_server()
    app.loop()
    app.stop_server()