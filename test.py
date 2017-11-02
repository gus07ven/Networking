
serverPrices = [ { 'provider' : 'Azure', 'network hourly cost': '.30', 'server hourly cost': '.114'},
                 {'provider': 'Google', 'network hourly cost': '.10', 'server hourly cost': '.100'},
                 {'provider': 'AWS', 'network hourly cost': '.20', 'server hourly cost': '.50'}]
    # 'Azure': ['network hourly cost': '.30', 'server hourly cost': '.114'],
    # 'Google': {'network hourly cost': '.15', 'server hourly cost': '.212'},
    # 'AWS': {'network hourly cost': '.10', 'server hourly cost': '.133'}


for server in serverPrices:
    network = server['network hourly cost']
    serverCost = server['server hourly cost']
    print network
    print serverCost


