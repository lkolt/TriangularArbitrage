import json

from collections import defaultdict

import sys

circle = input().replace(' ', '').split('->')


def calc_amount(am, is_print):
    if is_print:
        print('Amount:', am, circle[0])
    amount = am
    for i in range(len(circle) - 1):
        cur_val = circle[i]
        next_val = circle[i + 1]

        pair = cur_val + '_' + next_val
        reverse_pair = next_val + '_' + cur_val

        if pair in storage:
            ask_rate, ask_amount, _, _ = storage[pair]
            amount = min(ask_amount, amount)
            amount *= 1.0 / ask_rate

            if is_print:
                print(pair + ' OK')

        elif reverse_pair in storage:
            _, _, bid_rate, bid_amount = storage[reverse_pair]

            amount *= bid_rate
            amount = min(bid_amount, amount)
            if is_print:
                print(reverse_pair + ' reversed OK')
        else:
            print(pair + ' BAD')
            sys.exit(1)

        if is_print:
            print('Amount:', amount, next_val)
            print()
    return amount


with open('TestData.json', 'r') as file:
    data = json.loads(file.read())[0]

storage = defaultdict()

for currency_pair in data:
    ask_rate = float(data[currency_pair]['lowestAsk']['rate'])
    ask_amount = float(data[currency_pair]['lowestAsk']['amount'])
    bid_rate = float(data[currency_pair]['highestBid']['rate'])
    bid_amount = float(data[currency_pair]['highestBid']['amount'])

    storage[currency_pair] = (ask_rate, ask_amount, bid_rate, bid_amount)


res_amount = calc_amount(1e5, False)

amount = res_amount
for i in range(len(circle) - 2, -1, -1):
    cur_val = circle[i]
    next_val = circle[i + 1]

    pair = cur_val + '_' + next_val
    reverse_pair = next_val + '_' + cur_val

    if pair in storage:
        ask_rate, ask_amount, _, _ = storage[pair]
        amount /= 1.0 / ask_rate
    elif reverse_pair in storage:
        _, _, bid_rate, bid_amount = storage[reverse_pair]
        amount /= bid_rate

print('Profit:', calc_amount(amount, True) - amount)
