import SimpleHTTPServer
import SocketServer
import decimal
import socket
import time
import sys
import json
import requests
import urllib2
import os, errno

# For testing purposes
# serverPrices = [{'provider': 'Azure', 'network hourly cost': '.30', 'server hourly cost': '.114'},
#                 {'provider': 'Google', 'network hourly cost': '.15', 'server hourly cost': '.212'},
#                 {'provider': 'AWS', 'network hourly cost': '.10', 'server hourly cost': '.133'}]

servers = [
    {'provider': 'Google', 'ip': '104.199.113.30', 'port': 3828, 'rtt': 1000},
    # {'name': 'Azure', 'ip': '40.74.226.49', 'port': 2832, 'rtt': 1000},
    # {'name': 'AWS', 'ip': '18.221.224.159', 'port': 2830, 'rtt': 1000},
    # {'name': 'Local', 'ip': '192.168.56.1', 'port': 12345, 'rtt': 1000},
]


option = sys.argv[2]
userInputFilename = sys.argv[3]
decimal.getcontext().prec = 2

# "Ping" providers to get RTT
def pingProviders():
    print 'Performing network measurements...'
    rttPings = []
    for server in servers:
        clientSock = socket.socket()
        host = server.get('ip')
        port = server.get('port')
        clientSock.connect((host, port))
        print 'Connection established with: ' + host + ' in port: ' + str(port)
        pingPackage = {"Type": "ping"}
        ping = json.dumps(pingPackage)
        clientSock.send(ping)
        sendTime = int(round(time.time() * 1000))
        response = clientSock.recv(4096)
        recTime = int(round(time.time() * 1000))
        rtt = round(recTime - sendTime, 3)
        provider = server.get('provider')
        print provider, str(rtt), " ms"
        rttPings.append({'provider': server.get('name'), 'rtt': str(rtt)})
        server['rtt'] = rtt
        clientSock.close()
        downloadFile(provider, userInputFilename)
    return rttPings

# Call pricingAPI to calculate provider total cost
def calculatePrice():
    print '------------------------------------------------------------------------------------------------------------'
    print 'Performing total cost calculation...'
    # Connect to a cloud server to get prices
    url = 'http://104.199.113.30/costs'      #104.199.113.30
    r = requests.get(url)
    prices = r.content.encode('utf-8')
    dataList = json.loads(prices)             #json.loads(prices) # LocalDebug: serverPrices
    totalProviderCost = []
    for item in dataList:
        totalHourlyCost = decimal.Decimal(item['network hourly cost']) + decimal.Decimal(item['server hourly cost'])
        totalProviderCost.append({'provider': str(item['provider']), 'total cost': str(totalHourlyCost)})
    sortedValues = sorted(totalProviderCost, key=lambda t: t['total cost'])
    print sortedValues
    bestPriceProvider = str(sortedValues[0]['provider'])
    print 'Best choice based on price: ' + str(sortedValues[0]['provider'])
    print '------------------------------------------------------------------------------------------------------------'
    downloadFile(bestPriceProvider, userInputFilename)
    return sortedValues


def doBoth():
    print 'Finding best price and performance combination...'
    prices = calculatePrice()
    rttPings = pingProviders()
    bestCombo = []
    for provider in prices:
      for ping in rttPings:
          if ping['provider'] == provider['provider']:
            bestCombo.append({'provider': provider['provider'], 'cost':
                              str(decimal.Decimal(ping['rtt']) * decimal.Decimal(provider['total cost']))})
    sortedValues = sorted(bestCombo, key=lambda t: t['cost'])
    print 'With a total cost of ' + str(bestCombo[0]['cost']) + ' our best choice is ' + str(bestCombo[0]['provider'])
    downloadFile(provider, userInputFilename)
    return sortedValues

# Download files and save to folder
def downloadFile(provider, fileName):
    provider = 'Google'  # Debug
    print 'Getting ' + fileName + ' from ' + provider + '...'
    for server in servers:
        if server.get('provider') == provider:
            ip = server.get('ip')
    try:
        url = 'http://' + ip + "/UploadedFiles/" + fileName
        response = urllib2.urlopen(url)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), fileName)
        else:
            print 'Error in downloadFile'
    path = os.path.join(os.getcwd(), "DownloadedFilesM1")
    if not os.path.exists(path):
        os.mkdir(path, 0755)
    with open(os.path.join(path, fileName), "wb+") as f:
        f.write(response.read())
    print 'The file has been downloaded to the DownloadedFilesM1 folder'


# Take command line inputs
def readComInputs(option):
    try:
        if option == '-p':
            print 'Cost preference selected.'
            calculatePrice()
        elif option == '-n':
            print 'Network preference selected.'
            pingProviders()
        elif option == '-np':
            print 'Network and cost preference combined'
            doBoth()
        else:
            print 'Please enter -p for price, -n for network, or -np for price and network'
    except IndexError:
        print 'ERROR:\n' \
              'Please make sure to enter a flag to run the program.\n' \
              '-p to run based on price.\n' \
              '-n to run based on network measurements.\n' \
              '-np to run based on a combination of both.\n' \
              'Example: python programName flag\n' \
              'Where flag is either: -p, -n, or -np.'

def runProxyServer():
    readComInputs(option)
    # Create HTTP server
    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print("Proxy server running at PORT ", PORT)

    httpd.serve_forever()
    # while True:
    #     t = threading.Thread(target=proxyServerFlags())

if __name__ == '__main__':
    # Global variables
    try:
        runProxyServer()
    except IndexError:
        print 'ERROR:\n' \
          'Please make sure to enter a flag to run the program.\n' \
          '-p to run based on price.\n' \
          '-n to run based on network measurements.\n' \
          '-np to run based on a combination of both.\n' \
          'Example: python programName flag\n' \
          'Where flag is either: -p, -n, or -np.'
