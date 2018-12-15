# coding=utf-8

from bs4 import BeautifulSoup
import urllib2
import json


def getPortfolio():
    url = "http://cci30.com"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")

    IGNORE = 'IGNORE'
    LIMIT = 15

    constituentsDiv = soup.find('div', {'class': 'table-item', 'id': 'constituentsDiv'})
    # print constituentsDiv.prettify()

    alt_lst = []
    icons = constituentsDiv.find_all('div', {'class': 'icone-table'})
    for icon in icons:
        alt_lst.append(icon.find('img')['alt'])

    cap_lst = []
    caps = constituentsDiv.find_all('td', {'class': 'market-cap'})
    for cap in caps:
        cap_lst.append(float(cap.text.strip().replace('$', '').replace(',', '')))

    with open('symbols.json') as symbol_file:    
        symbols = json.load(symbol_file)

    portfolio = {}
    i = -1
    # convert token to binance symbol
    # ignore some token
    # make a portfolio
    total_cap = 0.0
    while len(portfolio) < LIMIT and i < len(alt_lst):
        i = i + 1
        alt = alt_lst[i]
        if alt in symbols and symbols[alt] == IGNORE:
            continue
        portfolio[alt] = cap_lst[i] ** 0.5
        total_cap += portfolio[alt]

    result = {}
    for alt in alt_lst:
        if alt in portfolio:
            result[alt] = portfolio[alt] / total_cap

    return result