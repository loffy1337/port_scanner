import math
import socket
from ipaddress import ip_address
from threading import Thread


def func_chunks_num(lst, c_num=400):
    """
    Функция делящая список портов для сканирования нескольких портов на устройтсве
    Input -> [1, 2, 3, 4, ... 800]
    Output -> [
        [1, 2],
        [3, 4],
        ...
        [799, 800]
    ]
    """
    n = math.ceil(len(lst) / c_num)

    for x in range(0, len(lst), n):
        e_c = lst[x:n + x]
        if len(e_c) < n:
            e_c = e_c + [None for y in range(n - len(e_c))]
        yield e_c


def validate_ip(addresses: list) -> list:
    """
    Функция отсеивающая неккоректно введенные IP-адреса
    Input -> ['192.168.0.1', '123', 'dasf', '192.168.0.109']
    Output -> ['192.168.0.1', '192.168.0.109']
    """
    ip_addresses = list()
    for address in addresses:
        try:
            ip = ip_address(address)
            ip_addresses.append(ip)
        except (ValueError, IndexError,):
            pass
    return ip_addresses


def validate_port(port: int) -> list:
    """
    Функция валидирующая диапозон сканируемых портов
    Input -> 68000 or -5000
    Output -> [1, 2, 3, ... 65535]
    Or
    Input -> 2000
    Output -> [1, 2, 3, ... 2000]
    """
    if port > 65535 or port < 1:
        return [i for i in range(1, 65536)]
    return [i for i in range(1, port+1)]


def scan_ports(ip: str, ports: list) -> None:
    """Функция сканирующая порт устройства"""
    for port in ports:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = connection.connect_ex((ip, port,))
            if con:
                pass
            else:
                print(f'Ip: {ip} | Порт: {port}')
                connection.close()
        except TypeError:
            pass


def scan_ip(ip: str, ports: list) -> None:
    """Функция создающая потоки для сканирования устройства"""
    ports = func_chunks_num(ports)
    for port in ports:
        th = Thread(target=scan_ports, args=(ip, port))
        th.start()
        th.join()


def main() -> None:
    try:
        # Ввод входных данных (IP-адресов, диапозон портов)
        ip_addresses = validate_ip(input('Введите IP-адреса для сканирования портов: ').split())
        port = validate_port(int(input('Введите порт, который будет являться окончанием диапозона сканирования: ')))
    except TypeError:
        print('Введенные данные некорректны')
    for ip in ip_addresses:
        scan_ip(str(ip), port)


if __name__ == '__main__':
    main()
