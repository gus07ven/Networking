import sys
import decimal
import socket
import time
import json
import requests
import datetime
from flask import Flask, g
app = Flask(__name__)


# Take command line inputs
option = None    # used to be option
userInputFilename = None

class ProxyServices:

    # Call API for servers info
    def getServers(self):
        serversList = []
        # Connect to a cloud server to get serversList
        url = 'http://13.65.151.216/servers' # Azure servers
        r = requests.get(url)
        server = r.content.encode('utf-8')
        serversList = json.loads(server)
        return serversList

    # Call API for prices info
    def getPrices(self):
        prices =[]
        url = 'http://104.199.113.30/costs'  # AWS costs
        r = requests.get(url)
        prices = r.content.encode('utf-8')
        pricesList = json.loads(prices)
        return pricesList

    # "Ping" providers to get RTT
    def pingProviders(self, serverList):
        print 'Performing network measurements...'
        rttPings = []
        for server in serverList:
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
            rttPings.append({'provider': server.get('provider'), 'rtt': str(rtt), 'ip': server.get('ip')})
            server['rtt'] = rtt
            clientSock.close()
        return rttPings

    # Call pricingAPI to calculate provider total cost
    def calculatePrice(self, priceList):
        print '--------------------------------------------------------------------------------------------------------'
        print 'Performing total cost calculation...'
        totalProviderCost = []
        for item in priceList:
            totalHourlyCost = decimal.Decimal(item['network hourly cost']) + decimal.Decimal(item['server hourly cost'])
            totalProviderCost.append({'provider': str(item['provider']), 'total cost': str(totalHourlyCost)})
        sortedValues = sorted(totalProviderCost, key=lambda t: t['total cost'])
        print sortedValues
        bestPriceProvider = str(sortedValues[0]['provider'])
        print 'Best choice based on price: ' + str(sortedValues[0]['provider'])
        print '--------------------------------------------------------------------------------------------------------'
        return sortedValues


    def doBoth(self, prices, rttPings):
        print 'Finding best price and performance combination...'
        # prices = calculatePrice()
        # rttPings = pingProviders()
        bestCombo = []
        for provider in prices:
          for ping in rttPings:
              if ping['provider'] == provider['provider']:
                bestCombo.append({'provider': provider['provider'], 'cost':
                                  str(decimal.Decimal(ping['rtt']) * decimal.Decimal(provider['total cost']))})
        sortedValues = sorted(bestCombo, key=lambda t: t['cost'])
        print 'With a total cost of ' + str(bestCombo[0]['cost']) + ' our best choice is ' + \
              str(bestCombo[0]['provider'])
        return sortedValues


@app.route('/<string:filename>', methods=['GET'])
def getFileFromServer(filename, provider, listOfServers):

    # networkResults = []
    # pricesResults = []
    # bothResults = []

    global option
    print option
    proxyServer = ProxyServices()
    serverList = proxyServer.getServers()
    priceList = proxyServer.getPrices()

    if option == '-p':
        print 'Cost preference selected.'
        pricesResults = proxyServer.calculatePrice(priceList)
        urlToGetFile = [pricesResults[0]]
        getRequest()
    elif option == '-n':
        print 'Network preference selected.'
        networkResults = proxyServer.pingProviders(serverList)
        urlToGetFile = [networkResults[0]]
        getRequest()
    elif option == '-np':
        print 'Network and cost preference combined'
        pricesResults = proxyServer.calculatePrice(priceList)
        networkResults = proxyServer.pingProviders(serverList)
        bothResults = proxyServer.doBoth(pricesResults, networkResults)
        urlToGetFile = [bothResults[0]]


    ipAdd = []
    for server in listOfServers:
        if server.get('provider') == provider[0]['provider']:
            ipAdd.append(server.get('ip'))
    url = 'http://' + ipAdd[0] + '/UploadedFiles/' + filename
    respon = requests.get(str(url))
    return respon.content


# Threading debugging
@app.route('/slow')
def slow():
    time.sleep(10)
    print 'inside slow'
    return json.dumps(datetime.datetime.now(), default=datetime_handler)


if __name__ == '__main__':

    decimal.getcontext().prec = 2
    option = sys.argv[1]
    print option

    try:
        if option == '-p':
            print 'Cost preference selected.'
            pricesResults = proxyServer.calculatePrice(priceList)
            urlToGetFile = [pricesResults[0]]
            getFileFromServer(urlToGetFile, serverList)
        elif option == '-n':
            print 'Network preference selected.'
            networkResults = proxyServer.pingProviders(serverList)
            urlToGetFile = [networkResults[0]]
            getFileFromServer(urlToGetFile, serverList)
        elif option == '-np':
            print 'Network and cost preference combined'
            pricesResults = proxyServer.calculatePrice(priceList)
            networkResults = proxyServer.pingProviders(serverList)
            bothResults = proxyServer.doBoth(pricesResults, networkResults)
            urlToGetFile = [bothResults[0]]
            getFileFromServer(urlToGetFile, serverList)
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

    import argparse

    parser = argparse.ArgumentParser(description='Development Server Help')
    # parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
    #                     help="run in debug mode (for use with PyCharm)", default=False)
    # parser.add_argument("-p", "--port", dest="port",
    #                     help="port of server (default:%(default)s)", type=int, default=5000)
    # parser.add_argument("-F", "--flag", dest="network", help="N for network, P for price, NP for both", type=str)
    cmd_args = parser.parse_args()
    app_options = {"port": "5000"}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False
        app_options["threaded"] = True

    app.run(**app_options)
