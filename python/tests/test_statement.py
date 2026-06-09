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
