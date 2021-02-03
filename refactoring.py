import math

def statement(invoice, plays):
    def play_for(aPerformace):
        # Remove temporary local variable. because temporary variables create a lot of locally scoped names that complicate extractions.
        # this change is unlikely to significantly affect performance
        # and even if it were, it is much easier to improve performance of a well-factored code base.
        return plays[aPerformace["playID"]]

    def amount_for(aPerformance):
        # it's calculating the charge for one performance
        # rename some of the variables to make them clearer
        # Any fool can write code that a computer can under stance. Good programmers write code that humans can understand

        if play_for(aPerformance)["type"] == "tragedy":
            result = 40000
            if aPerformance["audience"] > 30:
                result += 1000 * (aPerformance["audience"] - 30)
        elif play_for(aPerformance)["type"] == "comedy":
            result = 30000
            if aPerformance["audience"] > 20:
                result += 10000 + 500 * (aPerformance["audience"] - 20)
            result += 300 * aPerformance["audience"]
        else:
            raise ValueError("unknown type:" + play_for(aPerformance))

        return result

    def volume_credit_for(perf):
        volume_credits = max(perf["audience"] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play_for(perf)["type"]:
            volume_credits += math.ceil(perf["audience"])

        return volume_credits

    total_amount = 0

    result = f"Statement for {invoice['customer']}\n"
    for perf in invoice["performances"]:
        # print line for this order
        result += f"    {play_for(perf)['name']}: {amount_for(perf) / 100} ({perf['audience']} seats)\n"
        total_amount += amount_for(perf)

    volume_credits = 0
    for perf in invoice["performances"]:
        # add Volume credits
        volume_credits += volume_credit_for(perf)

    result += f"Amount owed is {total_amount / 100}\n"
    result += f"You earned {volume_credits} credits\n"
    return result


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
