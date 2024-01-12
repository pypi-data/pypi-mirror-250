import socket
routes = {}
def route(path): 
	'''Decorator that reports the execution time.'''

	def wrapper(func): 
		routes[path] = func
		return routes 
		
	return wrapper
def get_route(path, headers):
	if path in routes: return routes[path](headers)
	else: return '<h1>404</h1>'
def initServer(PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('localhost', PORT))
    except:
        initServer(PORT+1)
    server_socket.listen(1)
    print(f'Running on: http://localhost:{PORT}')
    while 1:
        connection, address = server_socket.accept()
        req = connection.recv(1024).decode()
        key_val = req.split(None)
        path = key_val[1]
        headers = {key.rstrip(':'): value for key, value in dict(zip(key_val[3:len(key_val)][0::2], key_val[3:len(key_val)][1::2])).items()}
        headers['method'] = key_val[0]
        res = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{get_route(path, headers)}'
        connection.send(res.encode('utf-8'))
        connection.close()