import socket

s = socket.socket()
host = socket.gethostname()
port = 4999

s.connect((host, port))
s.send('Message from client'.encode())
print(s.recv(1024).decode())
print(s.recv(4096))
s.close()