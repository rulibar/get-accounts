from binance.client import Client

class Keypair:
    def __init__(self, api, secret):
        self.api = api
        self.secret = secret

exchanges = dict()
exchanges["bin1"] = Keypair(
    "api key",
    "secret")
#exchanges["bin2"] = Keypair(
#    "api key",
#    "secret")

print("Binance Balance Checker")
BTCUSD = float(input("BTC USD price: "))

for e in exchanges:
    # cycle through exchanges
    print("Name: " + e)
    ex = exchanges[e]
    client = Client(ex.api, ex.secret)
    # get current prices
    data = client.get_all_tickers()
    prices = dict()
    for i in range(len(data)): prices[data[i]['symbol']] = float(data[i]['price'])
    # get account info
    data = client.get_account()
    data = data['balances']
    fol = dict()
    # cycle through coins, get portfolio
    for i in range(len(data)):
        asset = data[i]['asset']
        free = float(data[i]['free'])
        locked = float(data[i]['locked'])
        total = free + locked
        value = 0
        if asset + "BTC" in prices:
            value = total * prices[asset + "BTC"]
        elif asset + "USDT" in prices:
            value = total * prices[asset + "USDT"]
            value = value/prices['BTCUSDT']
        elif asset == "USDT":
            value = total/prices['BTCUSDT']
        else: print("Cannot calculate value of {} coins.".format(asset))
        if value != 0: fol[asset] = {'amt':total, 'btc_value':value}
    # output portfolio info in desired format
    total_btc_value = 0
    for asset in fol:
        amt = fol[asset]['amt']
        btc_value = fol[asset]['btc_value']
        total_btc_value += btc_value
        print("{}\t| {}\t\t| {}".format(asset, amt, btc_value))
    print("Total BTC value: " + str(total_btc_value))
    print("Total USD value: " + str(total_btc_value * BTCUSD))
    # pause, empty line
    input("Press ENTER to continue: ")
    print("")
