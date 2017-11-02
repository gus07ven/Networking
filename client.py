import socket
import json

jsonData = '{"filename": "test", "distribute": "yes", "content": "hello from the terminator serv"}'
jsonToPython = json.dumps(jsonData)
print jsonToPython

clientSocket = socket.socket()         # Create a socket object
host = '104.199.113.30'               # Get local machine name
port = 2828                           # Reserve a port for your service.

clientSocket.connect((host, port))
print 'Connection established'
print clientSocket.send(jsonToPython)
clientSocket.close()                    # Close the socket when done