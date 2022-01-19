import subprocess

processes = []
INFO = 'Выберете действие:' \
       'q - выйти\n' \
       's - запустить сервер и клиенты\n' \
       'x - закрыть все окна\n'

MAX_CLIENTS = 1
while True:
    action = input(INFO)

    if action == 'q':
        break
    elif action == 's':
        processes.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        processes.append(subprocess.Popen('python client.py -n test1', creationflags=subprocess.CREATE_NEW_CONSOLE))
        processes.append(subprocess.Popen('python client.py -n test2', creationflags=subprocess.CREATE_NEW_CONSOLE))
        processes.append(subprocess.Popen('python client.py -n test3', creationflags=subprocess.CREATE_NEW_CONSOLE))


    elif action == 'x':
        while processes:
            to_kill = processes.pop()
            to_kill.kill()
