import socket
import json
import datetime
from config import START_MESSAGE, END_MESSAGE

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
        # elements = [args, ] + [f'{key} = {value}' for key, value in kwargs.items()]
        # text = '\n'.join(elements)
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
        print(json_content)
        if json_content:
            # text = f'Message from the Polog:\n\n{text}'
            return json_content
        return 'Empty message from the Polog Client Socket.'

    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            message = START_MESSAGE + message + END_MESSAGE
            s.send(message.encode())
            data = s.recv(1024).decode()
            print(data)
            if data != 'Ok':
                raise Exception('Bad socket response')