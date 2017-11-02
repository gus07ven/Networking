from flask import Flask, jsonify, request, json

app = Flask(__name__)

serverPrices = [{'provider': 'Azure', 'network hourly cost': '.75', 'server hourly cost': '.114'},
                {'provider': 'Google', 'network hourly cost': '.05', 'server hourly cost': '.212'},
                {'provider': 'AWS', 'network hourly cost': '.55', 'server hourly cost': '.133'}]


# Old reliable
@app.route('/')
def rely():
    return 'I know old reliable will give me my costs'


# Get cost for all servers
@app.route('/costs', methods=['GET'])
def getAllPrices():
    return jsonify({serverPrices})


# Get price for one server
@app.route('/cost/<string:provider>', methods=['GET'])
def getOneServerPrice(provider):
    serv = [server for server in serverPrices if server['provider'] == provider]
    return jsonify({'server': serv[0]})


# Post one server/ Add a server
@app.route('/addcost', methods=['POST'])
def addOneServer():
    server = {'provider': request.json['provider'], 'network hourly cost': request.json['network hourly cost'],
              'server hourly cost': request.json['server hourly cost']}
    serverPrices.append(server)
    return jsonify({serverPrices})


# Update one server
@app.route('/cost/<string:provider>', methods=['PUT'])
def editOneServer(provider):
    serv = [server for server in serverPrices if server['provider'] == provider]
    serv[0]['provider'] = request.json['provider']
    serv[0]['network hourly cost'] = request.json['network hourly cost']
    serv[0]['server hourly cost'] = request.json['server hourly cost']
    return jsonify({serv[0]})


# Delete one server
@app.route('/cost/<string:provider>', methods=['DELETE'])
def removeOne(provider):
    serv = [server for server in serverPrices if server['provider'] == provider]
    serverPrices.remove(serv[0])
    return jsonify({serverPrices})


#Every below this line is to debug with Pycharm
if __name__ == "__main__":
import argparse

parser = argparse.ArgumentParser(description='Development Server Help')
parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                    help="run in debug mode (for use with PyCharm)", default=False)
parser.add_argument("-p", "--port", dest="port",
                    help="port of server (default:%(default)s)", type=int, default=5000)

cmd_args = parser.parse_args()
app_options = {"port": cmd_args.port}

if cmd_args.debug_mode:
    app_options["debug"] = True
    app_options["use_debugger"] = False
    app_options["use_reloader"] = False

app.run(**app_options)
