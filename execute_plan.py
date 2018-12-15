# coding=utf-8

from binance.client import Client
import json

with open('config.json') as config_file:    
    config = json.load(config_file)

api_key = config['api_key']
api_secret = config['api_secret']

client = Client(api_key, api_secret)

prices = client.get_all_tickers()

print '*' * 30
for p in prices:
    print p['symbol'], ',', 

print ''
print '*' * 30
print '!' * 10, 'PLAN', '!' * 10
print '*' * 30

price_dict = {}

for item in prices:
    price_dict[item['symbol']] = float(item['price'])

plan = {}
for line in open('plan.csv'):
    splits = line.split(',')
    symbol = splits[0].strip()
    ratio = float(splits[1].strip())
    plan[symbol] = ratio
    print symbol, ratio

print '*' * 30

valid = True

for symbol in plan:
    if symbol + 'BTC' not in price_dict:
        print 'symbol does not exist: ', symbol
        valid = False

if not valid:
    exit()

total = 0.0
info = client.get_account()
for item in info['balances']:
    if float(item['free']) > 0.0:
        if item['asset'] == 'BTC':
            k = 1.0
        else:
            symbol = item['asset'] + 'BTC'
            if symbol not in price_dict:
                continue
            k = price_dict[symbol]
        # ignore minor balances
        if float(item['free']) * k < 0.0001:
            continue
        print item['asset'], item['free'], float(item['free']) * k
        total += float(item['free']) * k

print '*' * 30
btc_price = price_dict['BTCUSDT']
print 'total', total, 'BTC,', btc_price * total, 'USDT'
print '*' * 30

min_notional_dict = {}
exchange_info = client.get_exchange_info()
for s in exchange_info['symbols']:
    filters = s['filters']
    for filter in filters:
        if filter['filterType'] == 'MIN_NOTIONAL':
            min_notional_dict[s['symbol']] = float(filter['minNotional'])

diff_moeny = 0.0
executions = []
for symbol in plan:
    ratio = plan[symbol]
    money = abs(ratio) * btc_price * total
    flag = 'YES'
    if (symbol + 'BTC') in min_notional_dict:
        if abs(ratio) * total < min_notional_dict[symbol + 'BTC']:
            flag = 'NO'
    amount = total
    amount = total * abs(ratio) / price_dict[symbol + 'BTC']
    if ratio > 0.0:
        print 'BUY', symbol, amount, ':', money, 'USDT', flag
        if flag == 'YES':
            executions.append([1, symbol, amount])
    else:
        print 'SELL', symbol, amount, ':', money, 'USDT', flag
        if flag == 'YES':
            executions.append([-1, symbol, amount])
    diff_moeny += money
print '*' * 30
print 'TOTAL TRADE', diff_moeny, 'USDT'
print '*' * 30
# first sell to BTC
# then buy from BTC
executions = sorted(executions, key=lambda x: x[0])
for exe in executions:
    print exe
print '!' * 30
answer = input("you really want to rebalance?")
if answer == 'Y' or answer == 'y':
    print 'executing...'
else:
    print 'exiting...'
    exit()

# os.remove("plan.csv")


