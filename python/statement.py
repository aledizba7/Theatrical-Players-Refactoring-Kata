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


def create_statement_data(invoice, plays):
    def enrich_performance(perf):
        play = play_for(perf, plays)
        return {
            'play': play,
            'audience': perf['audience'],
            'amount': amount_for(perf, play),
            'credits': calculate_credits(perf, play)
        }

    performances = [enrich_performance(perf) for perf in invoice['performances']]
    return {
        'customer': invoice['customer'],
        'performances': performances,
        'total_amount': sum(perf['amount'] for perf in performances),
        'total_volume_credits': sum(perf['credits'] for perf in performances)
    }


class StatementPrinter:
    def print(self, data):
        raise NotImplementedError()


class PlainTextPrinter(StatementPrinter):
    def print(self, data):
        result = f'Statement for {data["customer"]}\n'

        def format_as_dollars(amount):
            return f"${amount:0,.2f}"

        for perf in data['performances']:
            result += f' {perf["play"]["name"]}: {format_as_dollars(perf["amount"]/100)} ({perf["audience"]} seats)\n'

        result += f'Amount owed is {format_as_dollars(data["total_amount"]/100)}\n'
        result += f'You earned {data["total_volume_credits"]} credits\n'
        return result


class HTMLPrinter(StatementPrinter):
    def print(self, data):
        result = f'<h1>Statement for {data["customer"]}</h1>\n'
        result += '<table>\n'
        result += '<tr><th>play</th><th>seats</th><th>cost</th></tr>\n'

        def format_as_dollars(amount):
            return f"${amount:0,.2f}"

        for perf in data['performances']:
            result += f'  <tr><td>{perf["play"]["name"]}</td><td>{perf["audience"]}</td><td>{format_as_dollars(perf["amount"]/100)}</td></tr>\n'

        result += '</table>\n'
        result += f'<p>Amount owed is <em>{format_as_dollars(data["total_amount"]/100)}</em></p>\n'
        result += f'<p>You earned <em>{data["total_volume_credits"]}</em> credits</p>\n'
        return result


def statement(invoice, plays):
    return PlainTextPrinter().print(create_statement_data(invoice, plays))


def html_statement(invoice, plays):
    return HTMLPrinter().print(create_statement_data(invoice, plays))


