#!/usr/bin/env python3
from __future__ import absolute_import

import json
import socket
import sys

from functools import lru_cache

@lru_cache(maxsize=128)
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
    socket_client.close()
    return url_info


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <url>')
        sys.exit(1)

    # Один запрос на сервер
    for i in range(10):
        print(f'Received message is [{parse_url(sys.argv[1])}]')
