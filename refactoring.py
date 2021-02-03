import math

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
    def volume_credit_for(perf):
        result = max(perf["audience"] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == perf["play"]["type"]:
            result += math.ceil(perf["audience"])

        return result

    def play_for(aPerformace):
        # Remove temporary local variable. because temporary variables create a lot of locally scoped names that complicate extractions.
        # this change is unlikely to significantly affect performance
        # and even if it were, it is much easier to improve performance of a well-factored code base.
        return plays[aPerformace["playID"]]

    def amount_for(aPerformance):
        # it's calculating the charge for one performance
        # rename some of the variables to make them clearer
        # Any fool can write code that a computer can under stance. Good programmers write code that humans can understand

        if aPerformance["play"]["type"] == "tragedy":
            result = 40000
            if aPerformance["audience"] > 30:
                result += 1000 * (aPerformance["audience"] - 30)
        elif aPerformance["play"]["type"] == "comedy":
            result = 30000
            if aPerformance["audience"] > 20:
                result += 10000 + 500 * (aPerformance["audience"] - 20)
            result += 300 * aPerformance["audience"]
        else:
            raise ValueError("unknown type:" + aPerformance["play"]["type"])

        return result

    def enrich_performance(aPerformance):
        result = dict(aPerformance)
        result["play"] = play_for(result)
        result["amount"] = amount_for(result)
        result["volume_credit"] = volume_credit_for(result)
        return result

    def total_volume_credits(data):
        # replace loop with pipeline
        return sum(perf["volume_credit"] for perf in data["performances"])

    def total_amount(data):
        return sum([perf["amount"] for perf in data["performances"]])

    def create_statement_data(invoice):
        statement_data = {}
        # take the customer and add it to the intermediate object
        statement_data["customer"] = invoice["customer"]
        statement_data["performances"] = [enrich_performance(perf) for perf in invoice["performances"]]
        statement_data["total_amount"] = total_amount(statement_data)
        statement_data["total_volume_credits"] = total_volume_credits(statement_data)
        return statement_data

    return render_plain_text(create_statement_data(invoice))


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
