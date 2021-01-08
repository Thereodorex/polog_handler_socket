from config import HOST, PORT
from socket_handler import Server


def handler(args, **kwargs):
    print(args)
    print(kwargs)

def server_test():
    print("Server started.")
    app = Server(HOST, PORT)
    app.start_server()
    app.loop()
    app.stop_server()