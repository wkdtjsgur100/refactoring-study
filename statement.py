import math


def volume_credit_for(perf):
    result = max(perf["audience"] - 30, 0)
    # add extra credit for every ten comedy attendees
    if "comedy" == perf["play"]["type"]:
        result += math.ceil(perf["audience"])

    return result

def play_for(aPerformace, plays):
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

def enrich_performance(aPerformance, plays):
    result = dict(aPerformance)
    result["play"] = play_for(result, plays)
    result["amount"] = amount_for(result)
    result["volume_credit"] = volume_credit_for(result)
    return result

def total_volume_credits(data):
    # replace loop with pipeline
    return sum(perf["volume_credit"] for perf in data["performances"])

def total_amount(data):
    return sum([perf["amount"] for perf in data["performances"]])

def create_statement_data(invoice, plays):
    statement_data = {}
    # take the customer and add it to the intermediate object
    statement_data["customer"] = invoice["customer"]
    statement_data["performances"] = [enrich_performance(perf, plays) for perf in invoice["performances"]]
    statement_data["total_amount"] = total_amount(statement_data)
    statement_data["total_volume_credits"] = total_volume_credits(statement_data)
    return statement_data
