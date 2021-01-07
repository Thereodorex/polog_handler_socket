import socket
from handler.client.base import BaseHandler
from handler.client.socket_handler import SocketHandler

class Socket_Sender(BaseHandler):

    def __init__(self, host, port, alt=None, filter=None, only_errors=None, secondHandler=None):
        self.host = host
        self.port = port
        self.handler = SocketHandler(host, port)
        self.secondHandler = secondHandler
        self.filter = filter
        self.only_errors = only_errors
        self.alt = alt

    def __call__(self, args, **kwargs):
        """
        Благодаря этой функции объект класса является вызываемым.
        В случае неудачи при записи лога, выполняется функция alt, если она была указана при инициализации объекта.
        """
        return self.do(self.get_content(args, **kwargs))

    def do(self, content):
        """
        Здесь происходит "магия" - лог записывается или отправляется куда-то.
        Подразумевается, что content - уже полностью подготовленный и обработанный объект с данными (обычно строка, но не обязательно).

        Рекомендуем отделить класс, непосредственно работающий с низкоуровневым механизмом записи / отправки логов, от класса, унаследованного от BaseHandler, и здесь вызывать только какой-то его метод.
        """
        return self.handler.send(content)

    def get_content(self, args, **kwargs):
        """
        Метод, который возвращает объект, с которым что-то будет делать self.do().
        В большинстве реализаций обработчиков это будет специфически отформатированная строка.
        """
        return self.handler.get_text(args, **kwargs)
