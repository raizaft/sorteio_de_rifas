import sys
from servidor import Server

MESSAGE_SIZE = 1024
HOST = 'localhost'
PORT = 8888

if len(sys.argv) == 2:
    HOST = sys.argv[1]
elif len(sys.argv) == 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

server = Server(HOST, PORT, MESSAGE_SIZE)
server.start()