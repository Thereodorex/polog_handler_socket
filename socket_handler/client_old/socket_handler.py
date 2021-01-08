import socket
import json
import datetime

class SocketHandler:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _is_jsonable(self, obj):
        try:
            json.dumps(obj)
            return True
        except:
            return False
        return False

    def _to_json(self, obj):
        try:
            return json.dumps(obj)
        except:
            return None
        return str(obj)

    def get_text(self, args, **kwargs):
        for k, v in kwargs.items():
            if not self._is_jsonable(v):
                if isinstance(v, datetime.datetime):
                    kwargs[k] = ['datetime', v.isoformat()]
                else:
                    kwargs[k] = str(v)
        json_content = args
        if len(kwargs.items()):
            if args:
                json_content = [args, kwargs]
            else:
                json_content = kwargs
        json_content = self._to_json(json_content)
        if json_content:
            return json_content
        return 'Empty message from the Polog Client Socket.'

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