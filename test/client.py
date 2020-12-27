from socket_sender import Socket_Sender
import os

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

for i in range(10):
    pid = os.fork()
    if not pid:
        break
logger = Socket_Sender(HOST, PORT)

logger.do('First test string')