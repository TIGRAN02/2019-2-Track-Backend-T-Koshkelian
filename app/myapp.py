import datetime


def app(environ, start_response):
    data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')
    headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(data)))]
    start_response('200 OK', headers)
    return [data]

