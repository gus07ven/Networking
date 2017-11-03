import requests, sys, click
from flask import Flask, g
app = Flask(__name__)


@app.route('/<string:filename>', methods=['GET'])
def getFileFromServer(filename):
    url = 'http://104.199.113.30/UploadedFiles/' + filename
    respon = requests.get(str(url))
    return respon.content


#Every below this line is to debug with Pycharm
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)", default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int, default=5000)
    parser.add_argument("-F", "--flag", dest="network", help="N for network, P for price, NP for both", type=str)
    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False

    app.run(**app_options)
