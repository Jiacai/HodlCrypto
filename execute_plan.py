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
    if symbol == 'BTC':
        continue
    if symbol + 'BTC' not in price_dict:
        print 'symbol does not exist: ', symbol
        valid = False

if not valid:
    exit()
