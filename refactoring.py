from create_statement_data import create_statement_data


def render_plain_text(data):
    # split phase
    # one is calculating the data required for the statement
    # the other is rendering it into text or HTML

    result = f"Statement for {data['customer']}\n"
    # print line for this order
    for perf in data["performances"]:
        result += f"    {perf['play']['name']}: {perf['amount'] / 100} ({perf['audience']} seats)\n"

    result += f"Amount owed is {data['total_amount'] / 100}\n"
    result += f"You earned {data['total_volume_credits']} credits\n"
    return result

def statement(invoice, plays):
    return render_plain_text(create_statement_data(invoice, plays))


# make test code
assert statement(
    {
        "customer": "BigCo",
        "performances": [
            {
                "playID": "hamlet",
                "audience": 55
            },
            {
                "playID": "as-like",
                "audience": 35
            }
        ]
    },
    {
        "hamlet": {"name": "Hamlet", "type": "tragedy"},
        "as-like": {"name": "As You Like It", "type": "comedy"}
    }
) == """Statement for BigCo
    Hamlet: 650.0 (55 seats)
    As You Like It: 580.0 (35 seats)
Amount owed is 1230.0
You earned 65 credits
"""
