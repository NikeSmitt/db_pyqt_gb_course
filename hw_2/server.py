import argparse
import logging
import select
import sys
import time
from socket import AF_INET, SOCK_STREAM, socket
import project_logs.config.server_log_config

from common import utils
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH, ENCODING, RESPONSE, \
    ACTION, SENDER, TIME, MESSAGE_TEXT, MESSAGE, ACCOUNT_NAME, PRESENCE, DESTINATION, USER, RESPONSE_200, RESPONSE_400, \
    ERROR, EXIT

from decos import log

# получаем логгера
from hw_2.discriptors.port import Port
from hw_2.metaClasses.serverVerifier import ServerChecked
server_logger = logging.getLogger('server')

@log
def arg_parser() -> tuple:
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.a
    server_port = namespace.p

    return server_address, server_port


class Server(ServerChecked):

    port = Port()

    def __init__(self, listen_address: str, listen_port: int):

        server_logger.info(
            f'Запущен сервер, порт для подключений: {listen_port}, '
            f'адрес с которого принимаются подключения: {listen_address}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')

        self.port = listen_port
        self.server_sock = socket(AF_INET, SOCK_STREAM)
        # self.server_sock.connect('local')
        self.server_sock.bind((listen_address, self.port))
        self.server_sock.settimeout(0.5)

        self.server_sock.listen(MAX_CONNECTIONS)

        # список клиентов
        self.clients = []

        # очередь сообщений
        self.messages = []

        # Словарь, содержащий имена пользователей и соответствующие им сокеты.
        self.chat_usernames = dict()


    @log
    def create_server_response(self, message: dict) -> dict:
        if message.get('action') and message['action'] == 'presence':
            print(f'Клиент {message["user"]["account_name"]} в сети')
            response = {
                "response": 200,
                "alert": "Привет от сервера"
                }
            return response



    def is_presence_message(self, message: dict) -> bool:
        """Проверяет, что сообщение от пользователя является приветсвием"""
        server_logger.debug(f'Разбор сообщения от клиента : {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем
        return ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message



    def check_username_is_free(self, message: dict, registered_names: dict) -> bool:
        """Проверяем, что имя пользователя в чате не используется"""
        return message[USER][ACCOUNT_NAME] not in registered_names.keys()


    def is_regular_message(self, message: dict) -> bool:
        """Проверям, что это обычное сообщение от пользователя"""
        return ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message


    def is_exit_message(self, message: dict) -> bool:
        """Проверяем, что сообщение о выходе пользователя"""
        return ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message





    def run(self):


        while True:
            try:
                client_sock, client_address = self.server_sock.accept()
            except OSError as e:
                pass
            else:
                server_logger.info(f'Установлено соединение с {client_address}')
                self.clients.append(client_sock)

            receive_data_clients = []
            send_data_clients = []
            error_clients = []

            try:
                if self.clients:
                    receive_data_clients, send_data_clients, error_clients = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            # принимаем сообщение (в случае ошибки, исключаем клиента)
            for client_with_message in receive_data_clients:
                try:
                    client_message = utils.get_message(client_with_message)
                    if self.is_presence_message(client_message):
                        if self.check_username_is_free(client_message, self.chat_usernames):

                            # сохраняем пользователя и сокет
                            self.chat_usernames[client_message[USER][ACCOUNT_NAME]] = client_with_message
                            utils.send_message(client_with_message, RESPONSE_200)
                        else:

                            # имя уже используется
                            response = RESPONSE_400
                            response[ERROR] = 'Имя пользователя уже занято'
                            utils.send_message(client_with_message, response)
                            self.clients.remove(client_with_message)
                            client_with_message.close()

                    elif self.is_regular_message(client_message):
                        self.messages.append(client_message)

                    elif self.is_exit_message(client_message):
                        name = client_message[ACCOUNT_NAME]
                        self.clients.remove(self.chat_usernames[name])
                        self.chat_usernames[name].close()
                        del self.chat_usernames[name]

                    else:
                        # сообщение не кошерное
                        response = RESPONSE_400
                        response[ERROR] = 'Запрос некорректен.'
                        utils.send_message(client_with_message, response)

                except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError):
                    server_logger.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    self.clients.remove(client_with_message)

            for message in self.messages:
                try:
                    print(f'{message=}')
                    if message[DESTINATION] in self.chat_usernames and self.chat_usernames[message[DESTINATION]] in send_data_clients:
                        utils.send_message(self.chat_usernames[message[DESTINATION]], message)
                        server_logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                                    f'от пользователя {message[SENDER]}.')
                    elif message[DESTINATION] in self.chat_usernames and self.chat_usernames[message[DESTINATION]] not in send_data_clients:
                        raise ConnectionError
                    else:
                        server_logger.error(
                            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                            f'отправка сообщения невозможна.')
                except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError):
                    server_logger.info(f'Связь с клиентом с именем {message[DESTINATION]} была потеряна')
                    self.clients.remove(self.chat_usernames[message[DESTINATION]])
                    del self.chat_usernames[message[DESTINATION]]

            self.messages.clear()




if __name__ == "__main__":
    listen_address, listen_port = arg_parser()
    print(f'{listen_address=}, {listen_port=}')

    server = Server(listen_address, listen_port)
    server.run()
