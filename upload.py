# 1. Accept file name as command line argument
# 2. Use JSON to interact to encode file with metadata
# 3. Upload metadata and content to server.py with TCP
import sys
import os
import base64
import json
import socket

# Accept file name as command line argument
if(sys.argv[1]):
    file = open(sys.argv[1],'r')
    # Create metadata
    fileSize = os.stat(sys.argv[1])
    fileName = sys.argv[1]
    fileContent = file.read()
print fileName
print fileSize.st_size
print fileContent

# Encode content
encoded = base64.b64encode(fileContent)
print 'Encoded file content: ' + encoded

# Create JSON object
packageData = {"filename": fileName, "distribute": "True", "content": encoded}
dataToJson = json.dumps(packageData)
print dataToJson

# Establish TCP connection
clientSock = socket.socket()                  # Create a socket object
host = '13.65.151.216'                       #'104.199.113.30'
port = 2832                                   #12345  # Reserve a port for your service.

# Google: '104.199.113.30', 2828 and 3828
# AWS: '18.221.224.159', 2830
# Azure: '13.65.151.216', 2832

clientSock.connect((host, port))
print 'Connection established with: ' + host
clientSock.send(dataToJson)
clientSock.close()                   # Close the socket when done

