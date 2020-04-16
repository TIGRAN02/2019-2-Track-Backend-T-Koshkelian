#!/usr/bin/env python3

import json
import socket
import sys


def parse_url(url):
    socket_client = socket.socket()
    socket_client.connect(('localhost', 8090))
    url = f'{url}\r\n'
    socket_client.send(url.encode('utf8'))

    data = b''
    tmp = socket_client.recv(1024)
    while tmp:
        data += tmp
        tmp = socket_client.recv(1024)
    url_info = json.loads(data)
    print(f'Received message is [{url_info}]')
    socket_client.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <url>')
        sys.exit(1)
    parse_url(sys.argv[1])