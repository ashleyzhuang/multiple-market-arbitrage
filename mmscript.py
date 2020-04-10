import requests

response = requests.get('https://www.predictit.org/api/marketdata/all/')
data = response.json()

markets = data['markets']
cleaned = []
for i in range(len(markets)):
    consol = {'name': markets[i]['name'], 'cont': []}
    contracts = markets[i]['contracts']
    for j in range(len(contracts)):
        if contracts[j]['status'] == 'Open':
            temp = {'cont_name': contracts[j]['shortName'], 'Buy Yes': contracts[j]['bestBuyYesCost'], 'Buy No': contracts[j]['bestBuyNoCost'], 'Sell Yes': contracts[j]['bestSellYesCost'], 'Sell No': contracts[j]['bestSellNoCost']}
            consol['cont'].append(temp)
    cleaned.append(consol)
# buying no's strategy
possible_no = []
for mark in cleaned:
    contracts = mark['cont']
    tot = []
    for cont in contracts:
        if cont['Buy No'] != None:
            tot.append(cont['Buy No'])
    if tot:
        loss = min(tot)
        profit = 0
        for i in range(len(tot)):
            if tot[i] == loss:
                continue
            profit += 1 - tot[i]
        if profit >= loss:
            possible_no.append((mark, profit-loss))
possible_no.sort(key = lambda x: x[1], reverse=True)
print(possible_no)

    
# buying yes' strategy
possible_yes = []
for mark in cleaned:
    contracts = mark['cont']
    tot = []
    if len(contracts) == 1:
        continue
    for cont in contracts:
        if cont['Buy Yes'] != None:
            tot.append(cont['Buy Yes'])
    if tot:
        cost = sum(tot)
        if cost <= 1:
            possible_yes.append((mark, 1 - cost))
possible_yes.sort(key = lambda x: x[1], reverse=True)
print(possible_yes)
