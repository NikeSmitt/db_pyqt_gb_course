import json
from socket import socket

from common.variables import ENCODING, MAX_PACKAGE_LENGTH


def get_message(client: socket):
    """
    Получает, декодирует и загружает в словарь
    :param client: socket
    :return: dict
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        response = json.loads(encoded_response.decode(ENCODING))
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock: socket, message: dict):
    """
    Кодирует и отправляет сообщение
    :param sock: socket
    :param message: dict
    :return:
    """
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
