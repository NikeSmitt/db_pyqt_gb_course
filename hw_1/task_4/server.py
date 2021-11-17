
import logging
import select
import sys
import time
from socket import AF_INET, SOCK_STREAM, socket
import project_logs.config.server_log_config

from common import utils
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH, ENCODING, RESPONSE, \
    ACTION, SENDER, TIME, MESSAGE_TEXT, MESSAGE, ACCOUNT_NAME, PRESENCE

from decos import log

# получаем логгера
server_logger = logging.getLogger('server')


@log
def create_server_response(message: dict) -> dict:
    if message.get('action') and message['action'] == 'presence':
        print(f'Клиент {message["user"]["account_name"]} в сети')
        response = {
            "response": 200,
            "alert": "Привет от сервера"
            }
        return response


def create_response_message(message: dict) -> dict:
    server_logger.debug(f'Разбор сообщения от клиента: {message}')


def main():

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
            print(listen_address)
        else:
            listen_address = DEFAULT_IP_ADDRESS
    except IndexError as e:
        server_logger.critical('Не указан адрес после параметра -a')
        sys.exit(1)

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            print(listen_port)
            if 1024 < listen_port <= 65535:
                server_logger.critical(f'Запуск сервера с указанием невалидного порта {listen_port}'
                                       f'Используйте адреса с 1024 до 65535')
                raise ValueError

        else:
            listen_port = DEFAULT_PORT
    except IndexError as e:
        server_logger.critical(f'Запуск сервера с указанием невалидного порта'
                               f'Укажите порт после параметра -p')
        sys.exit(1)

    except ValueError as e:
        sys.exit(1)

    server_logger.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind((listen_address, listen_port))
    server_sock.settimeout(0.5)

    server_sock.listen(MAX_CONNECTIONS)

    # список клиентов
    clients = []

    # очередь сообщений
    messages = []

    while True:
        try:
            client_sock, client_address = server_sock.accept()
        except OSError as e:
            pass
        else:
            server_logger.info(f'Установлено соединение с {client_address}')
            clients.append(client_sock)

        receive_data_clients = []
        send_data_clients = []
        error_clients = []

        if clients:
            receive_data_clients, send_data_clients, error_clients = select.select(clients, clients, [], 0)

        for client_with_message in receive_data_clients:
            client_message = utils.get_message(client_with_message)
            if client_message[ACTION] == PRESENCE:
                utils.send_message(client_with_message, create_server_response(client_message))
            else:
                # messages.append((client_message[ACCOUNT_NAME], client_message[MESSAGE_TEXT]))
                messages.append(client_message)
                print('Сообщения от клиента')

        if messages and send_data_clients:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][ACCOUNT_NAME],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][MESSAGE_TEXT]
            }
            # message = {
            #     ACTION: MESSAGE,
            #     SENDER: 'spam',
            #     TIME: time.time(),
            #     MESSAGE_TEXT: 'spam'
            # }
            del messages[0]
            for waiting_client in send_data_clients:
                try:
                    utils.send_message(waiting_client, message)
                except Exception as e:
                    server_logger.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)




if __name__ == "__main__":
    main()
