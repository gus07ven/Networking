from flask import Flask, jsonify, request, os
app = Flask(__name__)


servers = [{'provider': 'Azure', 'ip': '40.74.226.49', 'port': 2832, 'rtt': 1000},
           {'provider': 'AWS', 'ip': '18.221.224.159', 'port': 2830, 'rtt': 1000},
           {'provider': 'Google', 'ip': '104.199.113.30', 'port': 3828, 'rtt': 1000}
           ]


# Old reliable
@app.route('/')
def rely():
    return 'The server API endpoints are: ' \
           '/servers :  GET list of all providers' \
           '/servers/<string:provider> : GET information for a specific provider' \
           '/server : POST or add a new server' \
           '/server/<string:provider> : PUT or update an existing server' \
           '/server/<string:provider> : DELETE an existing provider'


# Get all servers
@app.route('/servers', methods=['GET'])
def getAllServers():
    return jsonify({servers})


# Get one server
@app.route('/server/<string:provider>', methods=['GET'])
def getOneServer(provider):
    serv = [server for server in servers if server['provider'] == provider]
    return jsonify({'server': serv[0]})


# Post one server
@app.route('/server', methods=['POST'])
def addOneServer():
    server = {'name': request.json['provider'], 'ip': request.json['ip'], 'port': request.json['port']}
    servers.append(server)
    return jsonify({servers})


# Update one server
@app.route('/server/<string:provider>', methods=['PUT'])
def editOneServer(provider):
    serv = [server for server in servers if server['provider'] == provider]
    serv[0]['provider'] = request.json['provider']
    return jsonify({serv[0]})


# Delete one server
@app.route('/server/<string:provider>', methods=['DELETE'])
def removeOne(provider):
    serv = [server for server in servers if server['provider'] == provider]
    servers.remove(serv[0])
    return jsonify({'servers': servers})


# Every below this line is to debug with Pycharm
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


