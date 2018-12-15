# coding=utf-8

from binance.client import Client
import json

all_symbols = []
current_ptfl = {}
for line in open('current.csv'):
    splits = line.split(',')
    symbol = splits[0].strip()
    ratio = float(splits[1].strip())
    current_ptfl[symbol] = ratio
    if symbol not in all_symbols:
        all_symbols.append(symbol)

target_ptfl = {}
for line in open('target.csv'):
    splits = line.split(',')
    symbol = splits[0].strip()
    ratio = float(splits[1].strip())
    target_ptfl[symbol] = ratio
    if symbol not in all_symbols:
        all_symbols.append(symbol)

for symbol in all_symbols:
    current = 0.0
    if symbol in current_ptfl:
        current = current_ptfl[symbol]

    target = 0.0
    if symbol in target_ptfl:
        target = target_ptfl[symbol]

    diff = target - current
    print symbol, diff

