"""3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2. Но в данном
случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате (использовать модуль
tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:


Reachable
10.0.0.1
10.0.0.2
Unreachable
10.0.0.3
10.0.0.4
"""

import ipaddress
import subprocess
from tabulate import tabulate


def host_range_ping_tab(r: tuple):
    start, end = ipaddress.ip_address(r[0]), ipaddress.ip_address(r[1])
    if start > end:
        raise ValueError('Used bad ip range')

    current_ip = start
    processes = []
    while current_ip <= end:

        ping_p = subprocess.Popen(['ping', current_ip.compressed], stdout=subprocess.PIPE)
        processes.append((current_ip, ping_p))

        current_ip += 1

    accepted_hosts = []
    non_accepted_hosts = []

    for ip, p in processes:
        output = p.stdout.read()
        decoded_output = output.decode(encoding='IBM866')
        for row in decoded_output.split('\n'):
            if 'потерь' in row:
                row = row.strip()
                percent = row.split('%')[0][1:]
                if int(percent) < 100:
                    accepted_hosts.append((ip.compressed,))

                else:
                    non_accepted_hosts.append((ip.compressed,))

        p.terminate()

    print(tabulate(accepted_hosts, headers=('Reachable',)))
    print(tabulate(non_accepted_hosts, headers=('Unreachable',)))


if __name__ == '__main__':
    host_range_ping_tab(('192.168.1.1', '192.168.1.4'))




