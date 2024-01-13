import socket, json, threading
routes = {}

def view(path, methods=['GET']):
	def wrapper(func):
		routes[path] = {'func':func, 'methods':methods}
		return routes

	return wrapper

def create_response(path, headers):
	if path in routes:
		if not headers['method'] in routes[path]['methods']:
			return 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\nMethod Not Allowed'
		res = routes[path]['func'](headers)
		res_type = type(res).__name__
		if res_type == 'dict': return f'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{json.dumps(res)}'
		if res_type == 'str': return f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{res}'
	else:
		if '404' in routes:
			res = routes['404']['func'](headers)
			res_type = type(res).__name__
			if res_type == 'dict': return f'HTTP/1.1 404 Not Found\r\nContent-Type: application/json\r\n\r\n{json.dumps(res)}' 
			if res_type == 'str': return f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n{res}'
		else: return 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 Not Found'

def handle_connection(connection):
	req = connection.recv(1024).decode()
	key_val = req.split(None)
	if len(key_val) < 2:
		return connection.close()
	path = key_val[1]
	headers = {key.rstrip(':'): value for key, value in dict(zip(key_val[3:len(key_val)][0::2], key_val[3:len(key_val)][1::2])).items()}
	headers['method'] = key_val[0]
	res = create_response(path, headers)
	connection.send(res.encode('utf-8'))
	connection.close()

def initServer(PORT=3000, ADDRESS='localhost'):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		server_socket.bind((ADDRESS, PORT))
	except:
		initServer(PORT + 1)
	server_socket.listen(5)
	print(f'Running on: http://localhost:{PORT}')

	while True:
		connection, address = server_socket.accept()
		threading.Thread(target=handle_connection, args=(connection,)).start()

class router:	
	route = view
	listen = initServer

def App(): return router