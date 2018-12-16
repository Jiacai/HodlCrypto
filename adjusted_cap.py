# coding=utf-8

from bs4 import BeautifulSoup
import urllib2
import json


mapping = {
    'bitcoin': 'BTC',
    'ripple': 'XRP',
    'ethereum': 'ETH',
    'stellar': 'XLM',
    'eos': 'EOS',
    'bitcoin-cash': 'BCHABC',
    'litecoin': 'LTC',
    'tron': 'TRX',
    'cardano': 'ADA',
    'monero': 'XMR',
    'iota': 'IOTA',
    'binance-coin': 'BNB',
    'nem': 'XEM',
    'dash': 'DASH',
    'ethereum-classic': 'ETC',
    'neo': 'NEO',
    'zcash': 'ZEC',
    'maker': 'MKR',
    'dogecoin': 'DOGE',
    'tezos': 'XTZ',
    'vechain': 'VEN',
    'waves': 'WAVES',
    'omisego': 'OMG',
    'basic-attention-token': 'BAT',
    'qtum': 'QTUM',
}


LIMIT = 15

url = "http://sturgle.com/adjusted_cap.json"
content = urllib2.urlopen(url).read()
cap_lst = json.loads(content)

# with open('symbols.json') as symbol_file:    
#     symbols = json.load(symbol_file)

portfolio = {}
i = -1
# convert token to binance symbol
lines_of_text = []
total_cap = 0.0
while len(portfolio) < LIMIT and i < len(cap_lst):
    i = i + 1
    cap = cap_lst[i]
    alt = cap[0]
    if alt not in mapping:
        print "ERROR", alt
        exit()
        continue
    alt = mapping[alt]
    portfolio[alt] = cap[1] ** 0.5
    total_cap += portfolio[alt]

print '*' * 30
for cap in cap_lst:
    alt = mapping[cap[0]]
    if alt in portfolio:
        ratio = portfolio[alt] / total_cap
        text = str(alt) + ', ' + str(ratio) + '\n'
        print text.strip()
        lines_of_text.append(text)

fh = open('target.csv', 'w')
fh.writelines(lines_of_text) 
fh.close() 
