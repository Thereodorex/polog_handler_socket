import time
import pytest
from socket_sender import socket_sender
from polog import log, config


lst = []

class DependencyWrapper:
    def __init__(self, v1, v2):
        pass

    def send(self, message):
        lst.append(message)

config.add_handlers(socket_sender('0.0.0.0', '55555', socket_wrapper=DependencyWrapper))


def test_send_normal():
    """
    Проверяем, что что-то проходит через обработчик в DependencyWrapper.
    """
    log('hello')
    time.sleep(0.0001)
    assert lst[0]
    lst.pop()

def test_send_error():
    log('hello', exception=ValueError())
    time.sleep(0.0001)
    assert lst[0]
    lst.pop()