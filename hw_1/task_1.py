"""1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или
ip-адресом. В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции
ip_address(). """
import ipaddress
import re
import subprocess
from subprocess import CREATE_NEW_CONSOLE

import chardet


def host_ping(ip_list: list):

    address_description = ''
    processes = []
    for address in ip_list:
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", address):
            ip_address = ipaddress.ip_address(address)
            address_description = ip_address.compressed
        else:
            address_description = address
        ping_p = subprocess.Popen(['ping', address_description], stdout=subprocess.PIPE)
        processes.append(ping_p)


    for p in processes:
        output = p.stdout.read()
        decoded_output = output.decode(encoding='IBM866')
        for row in decoded_output.split('\n'):
            if 'потерь' in row:
                row = row.strip()
                percent = row.split('%')[0][1:]
                if int(percent) < 100:
                    print(f'{address_description} Узел доступен')
                else:
                    print(f'{address_description} Узел недоступен')
                    
        p.terminate()




if __name__ == "__main__":
    ip_s = ['192.168.1.1', '77.88.55.80', 'yandex.ru']
    host_ping(ip_s)
