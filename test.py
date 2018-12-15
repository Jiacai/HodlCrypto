# coding=utf-8

from binance.client import Client
import json

with open('config.json') as config_file:    
    config = json.load(config_file)

api_key = config['api_key']
api_secret = config['api_secret']

client = Client(api_key, api_secret)

prices = client.get_all_tickers()
print prices

price_dict = {}

for item in prices:
    price_dict[item['symbol']] = float(item['price'])

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
        print item['asset'], item['free'], float(item['free']) * k
