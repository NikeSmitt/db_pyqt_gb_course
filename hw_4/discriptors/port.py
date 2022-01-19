class Port:
    def __init__(self, port_number: int = 7777):
        self._port_number = port_number

    def __get__(self, instance, owner):
        return self._port_number

    def __set__(self, instance, value: int):
        if not (isinstance(value, int) and 0 <= value <= 65535):
            raise ValueError('Попытка запуска клиента с неподходящим номером порта')


