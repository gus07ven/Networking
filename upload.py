# 1. Accept file name as command line argument
# 2. Use JSON to interact to encode file with metadata
# 3. Upload metadata and content to server.py with TCP
import sys
import os
import base64
import json
import socket

# Accept file name as command line argument
if sys.argv[1]:
    file = open(sys.argv[1],'r')
    # Create metadata
    fileSize = os.stat(sys.argv[1])
    fileName = sys.argv[1]
    fileContent = file.read()

# Encode content
encoded = base64.b64encode(fileContent)

# Create JSON object
packageData = {"filename": fileName, "distribute": "True", "content": encoded}
dataToJson = json.dumps(packageData)
print dataToJson

# Establish TCP connection
clientSock = socket.socket()            # Google: '104.199.113.30', 2828 and 3828
host = '104.199.113.30'                 # AWS: '18.221.224.159', 2830
port = 3828                             # Azure: '13.65.151.216', 2832


clientSock.connect((host, port))
print 'Connection established with: ' + host
clientSock.send(dataToJson)
clientSock.close()
print 'File has been uploaded'
