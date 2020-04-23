import requests

cleaned_marks = []

# Loads market data from PredictIt API
def load_data():
    response = requests.get('https://www.predictit.org/api/marketdata/all/')
    data = response.json()

    markets = data['markets']
    for i in range(len(markets)):
        consol = {'id': markets[i]['id'], 'name': markets[i]['name'], 'cont': []}
        contracts = markets[i]['contracts']
        for j in range(len(contracts)):
            if contracts[j]['status'] == 'Open':
                temp = {'cont_name': contracts[j]['shortName'], 'Buy Yes': contracts[j]['bestBuyYesCost'], 'Buy No': contracts[j]['bestBuyNoCost'], 'Sell Yes': contracts[j]['bestSellYesCost'], 'Sell No': contracts[j]['bestSellNoCost']}
                consol['cont'].append(temp)
        cleaned_marks.append(consol)

# Detects arbitrage for a given market
# Returns tuple of profit for buying all no's and buying all yes's
def detect_arb(mark):
    contracts = mark['cont']
    prices_no = []
    prices_yes = []
    profit_no = None
    profit_yes = None

    for cont in contracts:
        if cont['Buy No'] != None:
            prices_no.append(cont['Buy No'])
        if cont['Buy Yes'] != None:
            prices_yes.append(cont['Buy Yes'])
    if prices_no:
        loss = sum(prices_no)
        gain = len(prices_no) - 1
        profit_no = round(gain - loss, 2)
    if prices_yes:
        cost = sum(prices_yes)
        profit_yes = round(1 - cost, 1)

    return profit_no, profit_yes

# Prints arbitrage report for a single market
def print_arb(mark):
    profit_no, profit_yes = detect_arb(mark)

    print('------------------------------------------------------------------')
    print('Market:', mark['name'], '\nID:', mark['id'])
    print()

    if profit_no and profit_no > 0:
        print('Buy No\'s: ARBITRAGE FOUND! :D')
    else:
        print('Buy No\'s: No Arbitrage :(')

    print('Profit: ', profit_no)
    print()

    if profit_yes and profit_yes > 0:
        print('Buy Yes\'s: ARBITRAGE FOUND! :D')
    else:
        print('Buy Yes\'s: No Arbitrage :(')

    print('Profit: ', profit_yes)
    print('------------------------------------------------------------------')

# Prints out all markets with arbitrage
def all_arbs():
    total = 0

    arb_no = []
    arb_yes = []

    for mark in cleaned_marks:
        profit_no, profit_yes = detect_arb(mark)
        if profit_no and profit_no > 0:
            arb_no.append((mark, profit_no))
        if profit_yes and profit_yes > 0:
            arb_no.append((mark, profit_yes))

    arb_no.sort(key = lambda x: x[1], reverse=True)
    arb_yes.sort(key = lambda x: x[1], reverse=True)

    for tup in arb_no:
        mark = tup[0]
        profit = tup[1]
        print('ID:', mark['id'], '\nMarket:', mark['name'], )
        print('Buying no\'s min profit:', profit)
        print()

    for tup in arb_yes:
        mark = tup[0]
        profit = tup[1]
        print('Market:', mark['name'], '\nID:', mark['id'])
        print('Buying yes\'s min profit:', profit)
        print()

    print('TOTAL instances of arbitrage:', len(arb_no) + len(arb_yes))

load_data()

# Main execution
while True:
    user_input = input('Market ID (-1 to exit, "all" for all markets): ')
    if user_input == 'all':
        all_arbs()
    else:
        market_id = int(user_input)

        if market_id == -1:
            break
        mark = next((m for m in cleaned_marks if m['id'] == market_id), None)

        if mark == None:
            print("Invalid Market ID")
        else:
            print_arb(mark)
