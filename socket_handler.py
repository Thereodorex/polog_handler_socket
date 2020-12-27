import socket

class SocketHandler:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.send(message.encode())

    def get_text(self, args, **kwargs):
        elements = [args,] + [f'{key} = {value}' for key, value in kwargs.items()]
        text = '\n'.join(elements)
        if text:
            text = f'Message from the Polog:\n\n{text}'
            return text
        return 'Empty message from the Polog.'

    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.send(message.encode())
            data = s.recv(1024).decode()
            print(data)
            if data != 'Ok':
                raise Exception('Bad socket response')