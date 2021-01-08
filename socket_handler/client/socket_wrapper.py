import socket


class SocketWrapper():

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                message += "\r\n\r\n"
                s.connect((self.host, self.port))
                s.send(message.encode())
                data = s.recv(1024).decode()
                if data != 'Ok':
                    raise Exception('Bad socket response')
        except:
            # Тут должен быть обработчик ошибок
            pass
