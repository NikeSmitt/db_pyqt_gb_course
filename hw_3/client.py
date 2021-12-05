import argparse
import json
import logging
import threading



import project_logs.config.client_log_config
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM

from common import utils
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ENCODING, MAX_PACKAGE_LENGTH, ACTION, PRESENCE, \
    ACCOUNT_NAME, MESSAGE_TEXT, SENDER, MESSAGE, DESTINATION, TIME, EXIT
from decos import log


# получаем логгера
from metaClasses.clientVerifier import ClientChecked



client_logger = logging.getLogger('client')


@log
def arg_parser() -> tuple:
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default='test1', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.a
    server_port = namespace.p
    client_name = namespace.name

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        client_logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    return server_address, server_port, client_name


class Client(ClientChecked):

    # s = socket(AF_INET, SOCK_STREAM)

    def __init__(self, server_address: str, server_port: int, client_name: str):
        self.server_address = server_address
        self.server_port = server_port
        self.name = client_name

        try:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            # self.client_socket.listen(4)
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            client_logger.error(f'Соединение с сервером {server_address} было потеряно.')
            sys.exit(1)


    @log
    def create_presence_request(self):
        account_name = self.name
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
    def process_response(self, data: bytes):
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
    def create_new_message(self):
        """
        Получаем от пользователя строку сообщения
        :return: dict
        """

        message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
        message_dict = {
            'action': 'message',
            'time': time.time(),
            'account_name': self.name,
            'message_text': message
        }
        client_logger.debug(f'Сформирован словарь сообщения: {message_dict}')
        return message_dict


    @log
    def parse_message(self, message: dict) -> str:
        """Парсим словарь сообщения от пользователя в строку"""
        name = message.get(SENDER)
        message_text = message.get(MESSAGE_TEXT)
        if not name:
            client_logger.error(f'Ошибка парсинга сообщения от пользователя: {message}')
            return f'Ошибка в полученном сообщении'
        return f'{name}: {message_text}'





    @log
    def getting_messages_from_server(self):
        """Обработчик сообщений от сервера"""
        while True:
            try:
                message = utils.get_message(self.client_socket)
                if message.get(ACTION) == MESSAGE and message.get(SENDER) and message.get(MESSAGE_TEXT) \
                        and message.get(DESTINATION) == self.name:

                    print(f'Получено сообщение от пользователя: {message[SENDER]}:\n'
                          f'{message[MESSAGE_TEXT]}')
                    client_logger.debug(f'Получено сообщение от пользователя: {message[SENDER]}:\n'
                          f'{message[MESSAGE_TEXT]}')
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, json.JSONDecodeError):
                client_logger.critical(f'Потеряно соединение с сервером.')
                break


    def print_help(self):
        """Функция выводящяя справку по использованию"""
        print(f'Имя пользователя: {self.name}')
        print('Поддерживаемые команды:')
        print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')


    @log
    def create_exit_message(self):
        """Функция создаёт словарь с сообщением о выходе"""
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.name
        }

    @log
    def create_message(self) -> dict:
        """Создание сообщения для отправки. Запрашивает кому отправить и текст сообщения"""
        to_user = input('Кому отправить сообщение: ')
        text_message = input('Tекст сообщения: ')
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.name,
            DESTINATION: to_user,
            TIME: time.time(),
            MESSAGE_TEXT: text_message
        }

        return message_dict


    @log
    def user_interactive(self):
        """Взаимодействие с пользователем"""
        self.print_help()
        while True:
            user_command = input('Введите команду: ')
            if user_command == 'message':
                message = self.create_message()
                try:
                    utils.send_message(self.client_socket, message)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_logger.critical('Соединение с сервером потеряно')
            elif user_command == 'help':
                self.print_help()
            elif user_command == 'exit':
                exit_message = self.create_exit_message()
                utils.send_message(self.client_socket, exit_message)
                client_logger.info('Завершение работы по команде пользователя.')
                # Задержка неоходима, чтобы успело уйти сообщение о выходе
                time.sleep(0.5)
                break
            else:
                print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')



    def run(self):

        try:
            self.client_socket.connect((server_address, server_port))
            client_logger.info(f'Соединение с клиентом установлено')


            presence_data = self.create_presence_request()
            client_logger.debug(f'Формирование сообщения для сервера {presence_data}')
            self.client_socket.send(presence_data)
            client_logger.info('Отправка сообщения на сервер')
            server_response = utils.get_message(self.client_socket)
            client_logger.info(f'Получено сообщение от сервера {server_response}')

        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            client_logger.error(f'Соединение с сервером {server_address} было потеряно.')
            sys.exit(1)

        else:
            # клиентский процесс приема сообщений
            receiver = threading.Thread(
                target=self.getting_messages_from_server,
                args=(),
                daemon=True)
            receiver.start()

            # отпрпвка сообщений и взаимодействие с пользователем
            user_interface = threading.Thread(
                target=self.user_interactive,
                args=(),
                daemon=True)
            user_interface.start()
            client_logger.debug('Запущены процессы')

            while True:
                time.sleep(1)
                if receiver.is_alive() and user_interface.is_alive():
                    continue
                break


if __name__ == "__main__":
    # Получаем из аргументов командной строки занчения
    server_address, server_port, client_name = arg_parser()

    # Создаем клиента и запускаем



    client = Client(server_address, server_port, client_name)
    client.run()


