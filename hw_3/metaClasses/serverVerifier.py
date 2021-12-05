import dis


class ServerVerifier(type):
    def __init__(cls, clsname, bases, clsdict):

        if '__init__' in clsdict:
            dis_init_rows = dis.Bytecode(clsdict['__init__']).dis().split('\n')
            # print(dis_init_rows)

            # отсутствие вызовов connect для сокетов

            filtered = list(
                filter(lambda row: 'LOAD_METHOD' in row and 'connect' in row, dis_init_rows))
            if len(filtered):
                raise AttributeError('Присутствие вызовов connect для сокетов')

            # использование сокетов для работы по TCP;
            filtered = list(
                filter(lambda row: 'LOAD_GLOBAL' in row and 'SOCK_STREAM' in row, dis_init_rows))
            if not len(filtered):
                raise AttributeError('Не использование сокетов для работы по TCP')

        type.__init__(cls, clsname, bases, clsdict)


class ServerChecked(metaclass=ServerVerifier):
    pass