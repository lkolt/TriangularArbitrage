import json
import urllib.request

from collections import defaultdict


storage = defaultdict(list)
fee = defaultdict(int)
fee['maker'] = 0.001
fee['taker'] = 0.002


def sub_fee(total, pos):
    return total - total * fee[pos]


data = json.load(urllib.request.urlopen("https://poloniex.com/public?command=returnTicker"))

for currency_pair in data:
    left_currency, right_currency = currency_pair.split('_')
    ask = float(data[currency_pair]['lowestAsk'])
    bid = float(data[currency_pair]['highestBid'])
    storage[left_currency].append((right_currency, ask, bid))

for left_currency in list(storage):
    for right_currency, lr_ask, lr_bid in storage[left_currency]:
        for mid_currency, lm_ask, lm_bid in storage[left_currency]:
            for check_currency, rm_ask, rm_bid in storage[right_currency]:
                if check_currency == mid_currency:
                    profit_ask = sub_fee(sub_fee(sub_fee(1.0 / rm_ask, 'maker') * lm_bid, 'maker') / lr_ask, 'maker')
                    if profit_ask > 1:
                        print('(ask) ' + left_currency + '_' + right_currency + ' < (bid) ' + left_currency + '_' + mid_currency + ' * (bid) ' + mid_currency + '_' + right_currency)
                        print('profit: ' + str(profit_ask - 1))

                    profit_bid = sub_fee(sub_fee(sub_fee(1.0 / rm_bid, 'maker') * lm_ask, 'maker') / lr_bid, 'maker')
                    if profit_bid < 1:
                        print('(bid) ' + left_currency + '_' + right_currency + ' > (ask) ' + left_currency + '_' + mid_currency + ' * (ask) ' + mid_currency + '_' + right_currency)
                        print('profit: ' + str(1 - profit_bid))
