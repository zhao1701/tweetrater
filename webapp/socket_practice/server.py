import socket

s = socket.socket()
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()
port = 4999
s.bind((host,port))

s.listen(5)
while True:
	connection, address = s.accept()
	print('Got connection from', address)
	msg = connection.recv(1024).decode()
	msg += '|Server says hi'
	connection.send(msg.encode())
	connection.send(25**2)
	connection.close()