import socket
import json
import base64
import os

servers = [{'name': 'Azure', 'ip': '13.65.151.216', 'port': 2832},
           {'name': 'AWS', 'ip': '18.221.224.159', 'port': 2830},
           {'name': 'Google', 'ip': '104.199.113.30', 'port': 2828}
           ]

serverName = 'Google'

# Distribute files to other servers
def distributeContent(file):
    for server in servers:
        if server.get('name') != serverName:
            clientSocket = socket.socket()
            host2 = server.get('ip')
            port2 = server.get('port')

            clientSocket.connect((host2, port2))
            print clientSocket.send(file)
            print 'File was sent to ' + server.get('name')
            clientSocket.close()


# Accept file upload from upload.py
serverSocket = socket.socket()
host = '104.199.113.30'    #socket.gethostname() '104.199.113.30'
port = 2828    #12345   2828
serverSocket.bind((host, port))
serverSocket.listen(5)
print 'Server is running...'

while True:
    connection, address = serverSocket.accept()
    print 'Connection established with: ', address
    data = connection.recv(1024)
    connection.sendall("Rep")
    jsonDecoded = json.loads(data)
    ping = jsonDecoded.get('Type')
    if ping != 'ping':
        encodedContent = jsonDecoded.get('content')
        decoded = base64.b64decode(jsonDecoded.get('content'))  # Decode content
        filename = jsonDecoded.get('filename')
        distribute = jsonDecoded.get('distribute')
        print 'Decoded file content: ' + decoded
        print 'File name: ' + filename
        print 'Distribute: ' + distribute
        folder = os.path.join(os.getcwd(), 'UploadedFiles')
        # Create directory to store file
        if not os.path.exists(folder):
            os.mkdir(folder, 0755)
        # Write file and save it
        if not os.path.exists(filename):
            contentInput = str(decoded)
            writeToFile = open(os.path.join(folder, filename), "w+")
            writeToFile.write(contentInput)
        if distribute == 'True':
            jsonDecoded['distribute'] = 'False'
            jsonToPython = json.dumps(jsonDecoded)
            print jsonToPython
            distributeContent(jsonToPython)
            print 'File has been distributed to other servers.'
    else:
        print "Ping received"
    connection.close()

