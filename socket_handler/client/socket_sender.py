import json
import datetime
from socket_handler.client.base import BaseHandler
from socket_handler.client.socket_wrapper import SocketWrapper


class socket_sender(BaseHandler):

    def __init__(self, host, port, alt=None, filter=None, only_errors=None, secondHandler=None, socket_wrapper=SocketWrapper):
        self.host = host
        self.port = port
        self.secondHandler = secondHandler
        self.filter = filter
        self.only_errors = only_errors
        self.alt = alt
        self.socket_wrapper = socket_wrapper(host, port)

    def __call__(self, args, **kwargs):
        """
        Благодаря этой функции объект класса является вызываемым.
        В случае неудачи при записи лога, выполняется функция alt, если она была указана при инициализации объекта.
        """
        return self.do(self.get_content(args, **kwargs))

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

    def do(self, message):
        """
        Здесь происходит "магия" - лог записывается или отправляется куда-то.
        Подразумевается, что content - уже полностью подготовленный и обработанный объект с данными (обычно строка, но не обязательно).

        Рекомендуем отделить класс, непосредственно работающий с низкоуровневым механизмом записи / отправки логов, от класса, унаследованного от BaseHandler, и здесь вызывать только какой-то его метод.
        """
        return self.socket_wrapper.send(message)

    def get_content(self, args, **kwargs):
        """
        Метод, который возвращает объект, с которым что-то будет делать self.do().
        В большинстве реализаций обработчиков это будет специфически отформатированная строка.
        """
        return self.get_text(args, **kwargs)