
import json
import logging
import project_logs.config.client_log_config
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM

from common import utils
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ENCODING, MAX_PACKAGE_LENGTH, ACTION, PRESENCE, \
    ACCOUNT_NAME, MESSAGE_TEXT, SENDER
from decos import log


# получаем логгера
client_logger = logging.getLogger('client')


@log
def create_presence_request():

    account_name = 'Guest'
    message = {
        ACTION: PRESENCE,
        'time': time.ctime(time.time()),
        'type': "status",
        "user": {
            "account_name": account_name,
            "status": 'Hello there!'
        }
    }
    client_logger.debug(f'Сформировано сообщение для пользователя {account_name}')
    return json.dumps(message).encode(ENCODING)


@log
def process_response(data: bytes):
    """
    Парсит ответ сервера
    :param data:
    :return:
    """

    message = json.loads(data.decode(ENCODING))
    client_logger.debug(f'Разбор сообщения от сервера {message}')
    if 'response' in message:
        if message['response'] == 200:
            return {200: 'Ok'}
        else:
            return {message['response']: "Error"}


@log
def create_new_message(account_name='Guest'):
    """
    Получаем от пользователя строку сообщения
    :return: dict
    """

    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    message_dict = {
        'action': 'message',
        'time': time.time(),
        'account_name': account_name,
        'message_text': message
    }
    client_logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def parse_message(message: dict) -> str:
    """Парсим словарь сообщения от пользователя в строку"""
    name = message.get(SENDER)
    message_text = message.get(MESSAGE_TEXT)
    if not name:
        client_logger.error(f'Ошибка парсинга сообщения от пользователя: {message}')
        return f'Ошибка в полученном сообщении'
    return f'{name}: {message_text}'

def main():

    try:
        if '-a' in sys.argv:
            server_address = sys.argv[sys.argv.index('-a') + 1]
            print(server_address)
        else:
            server_address = DEFAULT_IP_ADDRESS
    except IndexError:
        client_logger.critical('Не указан адрес после параметра -a')
        sys.exit(1)

    try:
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])

            if 1024 < server_port <= 65535:
                client_logger.critical(f'Запуск клиента с указанием невалидного порта {server_port}'
                                       f'Используйте адреса с 1024 до 65535')
                raise ValueError

        else:
            server_port = DEFAULT_PORT
    except IndexError:
        client_logger.critical(f'Запуск клиента с указанием невалидного порта'
                               f'Укажите порт после параметра -p')
        sys.exit(1)

    except ValueError:
        sys.exit(1)

    try:
        if '-m' in sys.argv:
            client_mode = sys.argv[sys.argv.index('-m') + 1]
        else:
            client_mode = 'listen'
        if client_mode not in ('listen', 'send'):
            client_logger.critical(f'Указан недопустимый режим работы {client_mode}, допустимые режимы: listen , send')
            sys.exit(1)

    except IndexError:
        client_logger.critical(f'Запуск клиента с указанием невалидного режима'
                               f'Укажите режима send / listen после параметра -m')
        sys.exit(1)

    try:

        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        client_logger.info(f'Соединение с клиентом установлено')
        presence_data = create_presence_request()
        client_logger.debug(f'Формирование сообщения для сервера {presence_data}')
        client_socket.send(presence_data)
        client_logger.info('Отправка сообщения на сервер')
        server_response = utils.get_message(client_socket)
        client_logger.info(f'Получено сообщение от сервера {server_response}')

    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
        client_logger.error(f'Соединение с сервером {server_address} было потеряно.')
        sys.exit(1)

    else:
        while True:
            if client_mode == 'send':
                print('Режим работы - отправка сообщений.')
            if client_mode == 'listen':
                print('Режим работы - приём сообщений.')

            if client_mode == 'listen':
                message = utils.get_message(client_socket)
                print(parse_message(message))
                # print(utils.get_message(client_socket))


            if client_mode == 'send':
                new_message = create_new_message()
                if new_message['message_text'] == '!!!':
                    client_socket.close()
                    client_logger.info('Соединение с сервером закрыто')
                utils.send_message(client_socket, new_message)


if __name__ == "__main__":
    main()
