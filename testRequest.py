# # imported the requests library
# import requests
#
# image_url = "http://192.168.56.1:8000/arepa.jpg"
#
# # URL of the image to be downloaded is defined as image_url
# r = requests.get(image_url)  # create HTTP response object
#
# # send a HTTP request to the server and save
# # the HTTP response in a response object called r
# with open("py_logo.png", 'wb') as f:
#     # Saving received content as a png file in
#     # binary format
#
#     # write the contents of the response (r.content)
#     # to a new file in binary mode.
#     f.write(r.content)

import sys, os, decimal
#
#
# serverPrices = [{'provider': 'Azure', 'network hourly cost': '.30', 'server hourly cost': '.114'},
#                 {'provider': 'Google', 'network hourly cost': '.15', 'server hourly cost': '.212'},
#                 {'provider': 'AWS', 'network hourly cost': '.10', 'server hourly cost': '.133'}]
#
#
# try:
#     option = sys.argv[2]
#     decimal.getcontext().prec = 2
#
#     if option == '-p':
#         print 'Performing price total cost calculation...'
#         totalPriceHour = {}
#         for server in serverPrices:
#             totalHourlyCost = decimal.Decimal(server.get('network hourly cost')) + \
#                               decimal.Decimal(server.get('server hourly cost'))
#             totalPriceHour[server.get('provider')] = totalHourlyCost
#         sortedValues = sorted(totalPriceHour.items(), key=lambda t: t[1])
#         print 'Based on price we will download file from: ' + sortedValues[0][0]
#
#     elif option == '-n':
#         print 'Network only'
#     elif option == '-np':
#         print 'Network and price combined'
#     else:
#         print 'Please enter -p for price, -n for network, or -np for price and network'
# except IndexError:
#     print 'ERROR:\n' \
#           'Please make sure to enter a flag to run the program.\n' \
#           '-p to run based on price.\n' \
#           '-n to run based on network measurements.\n' \
#           '-np to run based on a combination of both.\n' \
#           'Example: python programName flag\n' \
#           'Where flag is either: -p, -n, or -np.'

