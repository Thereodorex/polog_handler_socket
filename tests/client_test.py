import os
from socket_handler.client.socket_sender import socket_sender
from config import HOST, PORT

from polog import config
from polog import flog

config.add_handlers(socket_sender(HOST, PORT))

@flog
def logged_func(arg):
    return arg

def client_test():
    for i in range(10):
        pid = os.fork()
        if not pid:
            break
    logged_func(str(i) + ' test string')