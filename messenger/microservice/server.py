#!/usr/bin/env python3

import json
import socket

import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from bs4 import BeautifulSoup


def check_url(url):
    valid = URLValidator()
    try:
        valid(url)
    except ValidationError:
        print('Invalid URL')
        return False

    return True


def scrape_url(url):
    if not check_url(url.decode('utf8')):
        return json.dumps({'error': 'Invalid or unreachable URl', 'status': 400})

    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}
    for field in ['url', 'title', 'image', 'description', 'type']:
        try:
            field_content = soup.find('meta', property=f'og:{field}').get('content')
            result[field] = field_content
        except:
            continue
    return json.dumps(result)


def main():
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(('', 8090))
    socket_server.listen(50)
    while True:
        try:
            socket_client, address = socket_server.accept()
            data = b''
            tmp = socket_client.recv(1024)
            while tmp:
                data += tmp
                if tmp.endswith(b'\r\n'):
                    break
                tmp = socket_client.recv(1024)
            content = data.strip()
            url_info = scrape_url(content)

            print(f'Sending content [{content.decode("utf8")}]')
            socket_client.send(url_info.encode('utf8'))
            socket_client.close()
        except:
            break
    socket_server.close()


if __name__ == '__main__':
    main()
