import socket
import json
import base64


# Distribute files to other servers
def distributeContent(file):
    for name, ip, porter in servers:
        clientSocket = socket.socket()  # Create a socket object
        host = socket.gethostname()     # Get local machine name
        portCon = porter                  # Reserve a port for your service.

        clientSocket.connect((host, port))
        print clientSocket.send(file)
        clientSocket.close()


# Accept file upload from upload.py
serverSocket = socket.socket()
host = socket.gethostname()
port = 5555
serverSocket.bind((host, port))
serverSocket.listen(5)

while True:
    connection, address = serverSocket.accept()
    print 'Connection established with: ', address
    data = connection.recv(1024)
    jsonDecoded = json.loads(data)
    encodedContent = jsonDecoded.get('content')
    decoded = base64.b64decode(jsonDecoded.get('content'))  # Decode content
    filename = jsonDecoded.get('filename')
    distribute = jsonDecoded.get('distribute')
    print 'Decoded file content: ' + decoded
    print 'File name: ' + filename
    print 'Distribute: ' + distribute
    if distribute == 'True':
        jsonDecoded['distribute'] = 'False'
        distributeContent(jsonDecoded)
    connection.close()

