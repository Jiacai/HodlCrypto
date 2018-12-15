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

price_dict = {}

for item in prices:
    price_dict[item['symbol']] = float(item['price'])

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
# print current portfolio
lines_of_text = []
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
        text = str(item['asset']) + ', ' + str(float(item['free']) * k / total)
        lines_of_text.append(text)

fh = open('current.csv', 'w')
fh.writelines(lines_of_text) 
fh.close() 
