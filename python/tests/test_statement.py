import json

import pytest
from approvaltests import verify
from approval_utilities.utils import get_adjacent_file

from statement import statement


def test_example_statement():
    with open(get_adjacent_file("invoice.json")) as f:
        invoice = json.loads(f.read())
    with open(get_adjacent_file("plays.json")) as f:
        plays = json.loads(f.read())
    verify(statement(invoice, plays))


def test_statement_with_new_play_types():
    with open(get_adjacent_file("invoice_new_plays.json")) as f:
        invoice = json.loads(f.read())
    with open(get_adjacent_file("new_plays.json")) as f:
        plays = json.loads(f.read())
    with pytest.raises(ValueError) as exception_info:
        statement(invoice, plays)
    assert "unknown type" in str(exception_info.value)


def test_html_statement():
    from statement import html_statement
    with open(get_adjacent_file("invoice.json")) as f:
        invoice = json.loads(f.read())
    with open(get_adjacent_file("plays.json")) as f:
        plays = json.loads(f.read())
    expected = (
        "<h1>Statement for BigCo</h1>\n"
        "<table>\n"
        "<tr><th>play</th><th>seats</th><th>cost</th></tr>\n"
        "  <tr><td>Hamlet</td><td>55</td><td>$650.00</td></tr>\n"
        "  <tr><td>As You Like It</td><td>35</td><td>$580.00</td></tr>\n"
        "  <tr><td>Othello</td><td>40</td><td>$500.00</td></tr>\n"
        "</table>\n"
        "<p>Amount owed is <em>$1,730.00</em></p>\n"
        "<p>You earned <em>47</em> credits</p>\n"
    )
    assert html_statement(invoice, plays) == expected


def test_tragedy_calculator():
    from statement import TragedyCalculator
    # audience = 20 (<= 30)
    calc_small = TragedyCalculator({"audience": 20}, {"type": "tragedy"})
    assert calc_small.amount() == 40000
    assert calc_small.volume_credits() == 0

    # audience = 35 (> 30)
    calc_large = TragedyCalculator({"audience": 35}, {"type": "tragedy"})
    assert calc_large.amount() == 45000
    assert calc_large.volume_credits() == 5


def test_comedy_calculator():
    from statement import ComedyCalculator
    # audience = 15 (<= 20)
    calc_small = ComedyCalculator({"audience": 15}, {"type": "comedy"})
    assert calc_small.amount() == 34500  # 30000 + 300 * 15
    assert calc_small.volume_credits() == 3  # 0 + 15 // 5

    # audience = 25 (> 20)
    calc_large = ComedyCalculator({"audience": 25}, {"type": "comedy"})
    assert calc_large.amount() == 50000  # 30000 + 10000 + 500 * 5 + 300 * 25
    assert calc_large.volume_credits() == 5  # 0 + 25 // 5


def test_history_calculator():
    from statement import HistoryCalculator
    # audience = 20 (<= 30)
    calc_small = HistoryCalculator({"audience": 20}, {"type": "history"})
    assert calc_small.amount() == 50000
    assert calc_small.volume_credits() == 2  # 0 + 20 // 10

    # audience = 35 (> 30)
    calc_large = HistoryCalculator({"audience": 35}, {"type": "history"})
    assert calc_large.amount() == 57500  # 50000 + 1500 * 5
    assert calc_large.volume_credits() == 8  # 5 + 35 // 10


def test_pastoral_calculator():
    from statement import PastoralCalculator
    # audience = 10 (<= 15)
    calc_small = PastoralCalculator({"audience": 10}, {"type": "pastoral"})
    assert calc_small.amount() == 25000
    assert calc_small.volume_credits() == 1  # 0 + 10 // 8

    # audience = 20 (> 15)
    calc_large = PastoralCalculator({"audience": 20}, {"type": "pastoral"})
    assert calc_large.amount() == 29000  # 25000 + 800 * 5
    assert calc_large.volume_credits() == 2  # 0 + 20 // 8

