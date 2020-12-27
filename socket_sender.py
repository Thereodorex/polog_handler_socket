import socket
from base import BaseHandler
from socket_handler import SocketHandler

class Socket_Sender(BaseHandler):

    def __init__(self, host, port, alt=None, filter=None, only_errors=None):
        self.host = host
        self.port = port
        self.handler = SocketHandler(host, port)

    def do(self, content):
        """
        Здесь происходит "магия" - лог записывается или отправляется куда-то.
        Подразумевается, что content - уже полностью подготовленный и обработанный объект с данными (обычно строка, но не обязательно).

        Рекомендуем отделить класс, непосредственно работающий с низкоуровневым механизмом записи / отправки логов, от класса, унаследованного от BaseHandler, и здесь вызывать только какой-то его метод.
        """
        return self.handler.send(self.get_content(content))

    def get_content(self, args, **kwargs):
        """
        Метод, который возвращает объект, с которым что-то будет делать self.do().
        В большинстве реализаций обработчиков это будет специфически отформатированная строка.
        """
        return self.handler.get_text(args, **kwargs)
