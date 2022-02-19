"""
Get Accounts
get_accounts.py v1.1.2 (22-2-19)
Get holdings from Binance and sort by BTC value.

v1.1.1 (19-7-20)
- Initial working version

v1.1.2 (22-2-19)
- Sort entries by BTC value
- Update formatting

"""

from binance.client import Client

class Keypair:
    def __init__(self, api, secret):
        self.api = api
        self.secret = secret

exchanges = dict()
exchanges["bin1"] = Keypair(
    "api_key",
    "api_secret")
#exchanges["bin2"] = Keypair(
#    "api_key",
#    "api_secret")

print("Binance Balance Checker")
BTCUSD = float(input("BTC USD price: "))

for e in exchanges:
    # cycle through exchanges
    print("Name: " + e)
    ex = exchanges[e]
    client = Client(ex.api, ex.secret, tld='us')
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
    balances_str = list()
    for asset in fol:
        amt = fol[asset]['amt']
        btc_value = fol[asset]['btc_value']
        total_btc_value += btc_value
        balances_str.append([str(asset), "{:.8f}".format(amt)[:10], "{:.8f}".format(btc_value)[:10]])
    balances_str.sort(key=lambda x:float(x[2]), reverse=True)
    balances_str = ["\t| ".join(line) for line in balances_str]
    balances_str = "\n".join(balances_str)
    print(balances_str)
    print("Total BTC value: " + str(total_btc_value))
    print("Total USD value: " + str(total_btc_value * BTCUSD))
    input("Press ENTER to continue: ")
