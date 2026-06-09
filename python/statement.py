import math


class PlayCalculator:
    def __init__(self, performance, play):
        self.performance = performance
        self.play = play

    def amount(self):
        raise NotImplementedError()

    def volume_credits(self):
        raise NotImplementedError()


class TragedyCalculator(PlayCalculator):
    def amount(self):
        result = 40000
        if self.performance['audience'] > 30:
            result += 1000 * (self.performance['audience'] - 30)
        return result

    def volume_credits(self):
        return max(self.performance['audience'] - 30, 0)


class ComedyCalculator(PlayCalculator):
    def amount(self):
        result = 30000
        if self.performance['audience'] > 20:
            result += 10000 + 500 * (self.performance['audience'] - 20)
        result += 300 * self.performance['audience']
        return result

    def volume_credits(self):
        return max(self.performance['audience'] - 30, 0) + math.floor(self.performance['audience'] / 5)


def create_play_calculator(performance, play):
    if play['type'] == "tragedy":
        return TragedyCalculator(performance, play)
    elif play['type'] == "comedy":
        return ComedyCalculator(performance, play)
    else:
        raise ValueError(f"unknown type: {play['type']}")


def calculate_credits(perf, play):
    return create_play_calculator(perf, play).volume_credits()


def amount_for(perf, play):
    return create_play_calculator(perf, play).amount()


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


