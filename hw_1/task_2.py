"""Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только
последний октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение. """
import ipaddress
import subprocess

from task_1 import host_ping


def host_range_ping(r: tuple):
    start, end = ipaddress.ip_address(r[0]), ipaddress.ip_address(r[1])
    if start > end:
        raise ValueError('Used bad ip range')

    current_ip = start
    processes = []
    while current_ip <= end:

        ping_p = subprocess.Popen(['ping', current_ip.compressed], stdout=subprocess.PIPE)
        processes.append((current_ip, ping_p))

        current_ip += 1



    for ip, p in processes:
        output = p.stdout.read()
        decoded_output = output.decode(encoding='IBM866')
        for row in decoded_output.split('\n'):
            if 'потерь' in row:
                row = row.strip()
                percent = row.split('%')[0][1:]
                if int(percent) < 100:
                    print(f'{ip.compressed} Узел доступен')
                else:
                    print(f'{ip.compressed} Узел недоступен')

        p.terminate()



if __name__ == "__main__":
    # host_range_ping(('192.168.1.1', '192.168.1.0'))
    host_range_ping(('192.168.1.1', '192.168.1.2'))
