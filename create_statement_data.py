from statement import play_for, amount_for, volume_credit_for, total_amount, total_volume_credits


def enrich_performance(aPerformance, plays):
    result = dict(aPerformance)
    result["play"] = play_for(result, plays)
    result["amount"] = amount_for(result)
    result["volume_credit"] = volume_credit_for(result)
    return result


def create_statement_data(invoice, plays):
    statement_data = {}
    # take the customer and add it to the intermediate object
    statement_data["customer"] = invoice["customer"]
    statement_data["performances"] = [enrich_performance(perf, plays) for perf in invoice["performances"]]
    statement_data["total_amount"] = total_amount(statement_data)
    statement_data["total_volume_credits"] = total_volume_credits(statement_data)
    return statement_data
