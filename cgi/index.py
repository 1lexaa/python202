#!C:/Python/python.exe

import cgi
import os

form = cgi.FieldStorage()
x = form.getvalue('x', '')
y = form.getvalue('y', '')

request_uri = os.environ.get('REQUEST_URI', '/')
request_method = os.environ.get('REQUEST_METHOD', 'GET')
remote_addr = os.environ.get('REMOTE_ADDR', '127.0.0.1')
request_scheme = os.environ.get('REQUEST_SCHEME', 'http')

envs = f"<ul><li>REQUEST_URI = {request_uri}</li><li>REQUEST_METHOD = {request_method}</li><li>REMOTE_ADDR = {remote_addr}</li><li>REQUEST_SCHEME = {request_scheme}</li></ul>"

print("Content-Type: text/html; charset=cp1251")
print("Connection: close")
print()

print(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="cp1251">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CGI</title>
</head>
<body>
    <h1>CGI is running</h1>
    <p>{envs}</p>
    <p>Query String: {{'x': '{x}', 'y': '{y}'}}</p>
</body>
</html>''')