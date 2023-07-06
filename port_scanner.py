import math
import socket
from ipaddress import ip_address
from threading import Thread


def func_chunks_num(lst, c_num=400):
    n = math.ceil(len(lst) / c_num)

    for x in range(0, len(lst), n):
        e_c = lst[x:n + x]
        if len(e_c) < n:
            e_c = e_c + [None for y in range(n - len(e_c))]
        yield e_c


def validate_ip(addresses: list) -> list:
    ip_addresses = list()
    for address in addresses:
        try:
            ip = ip_address(address)
            ip_addresses.append(ip)
        except (ValueError, IndexError,):
            pass
    return ip_addresses


def validate_port(port: int) -> list:
    if port > 15000 or port < 1:
        return [i for i in range(1, 15000)]
    return [i for i in range(1, port+1)]


def scan_ports(ip: str, ports: list) -> None:
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in ports:
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
    ports = func_chunks_num(ports)
    for port in ports:
        th = Thread(target=scan_ports, args=(ip, port))
        th.start()
        th.join()


def main() -> None:
    try:
        ip_addresses = validate_ip(input('Введите IP-адреса для сканирования портов: ').split())
        port = validate_port(int(input('Введите порт, который будет являться окончанием диапозона сканирования: ')))
    except TypeError:
        print('Введенные данные некорректны')
    for ip in ip_addresses:
        scan_ip(str(ip), port)


if __name__ == '__main__':
    main()
