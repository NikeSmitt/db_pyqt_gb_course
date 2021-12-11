import dis
from socket import socket


class ClientVerifier(type):

    def __init__(cls, clsname, bases, clsdict):
        for key, value in clsdict.items():
            if isinstance(value, socket):
                raise AttributeError('Запрещено создание сокета на уровне класса')

        if '__init__' in clsdict:
            dis_init_rows = dis.Bytecode(clsdict['__init__']).dis().split('\n')
            # print(dis_init_rows)

            # отсутствие вызовов accept и listen для сокетов;

            filtered = list(filter(lambda row: 'LOAD_METHOD' in row and 'bind' in row or 'listen' in row, dis_init_rows))
            if len(filtered):
                raise AttributeError('Присутствие вызовов accept и listen для сокетов')

            # использование сокетов для работы по TCP;
            filtered = list(
                filter(lambda row: 'LOAD_GLOBAL' in row and 'SOCK_STREAM' in row, dis_init_rows))
            if not len(filtered):
                raise AttributeError('Не использование сокетов для работы по TCP')
        type.__init__(cls, clsname, bases, clsdict)






class ClientChecked(metaclass=ClientVerifier):
    pass
