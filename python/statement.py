import math


def calculate_credits(perf, play):
    result = max(perf['audience'] - 30, 0)
    if play['type'] == "comedy":
        result += math.floor(perf['audience'] / 5)
    return result


def amount_for(perf, play):
    if play['type'] == "tragedy":
        result = 40000
        if perf['audience'] > 30:
            result += 1000 * (perf['audience'] - 30)
    elif play['type'] == "comedy":
        result = 30000
        if perf['audience'] > 20:
            result += 10000 + 500 * (perf['audience'] - 20)
        result += 300 * perf['audience']
    else:
        raise ValueError(f'unknown type: {play["type"]}')
    return result


def play_for(perf, plays):
    return plays[perf['playID']]


def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    def format_as_dollars(amount):
        return f"${amount:0,.2f}"

    for perf in invoice['performances']:
        # add volume credits
        volume_credits += calculate_credits(perf, play_for(perf, plays))
        # print line for this order
        result += f' {play_for(perf, plays)["name"]}: {format_as_dollars(amount_for(perf, play_for(perf, plays))/100)} ({perf["audience"]} seats)\n'
        total_amount += amount_for(perf, play_for(perf, plays))

    result += f'Amount owed is {format_as_dollars(total_amount/100)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result


