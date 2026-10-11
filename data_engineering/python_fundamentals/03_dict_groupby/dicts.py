def dict_groupby(data):

    result = {}

    for row in data:
        if row["region"] in result:

            result[row["region"]] = result[row["region"]] + row["amount"]

        else:

            result[row["region"]] = row["amount"]

    return result

sales = [
    {"region": "West", "product": "Widget", "amount": 120},
    {"region": "East", "product": "Widget", "amount": 85},
    {"region": "West", "product": "Gadget", "amount": 200},
    {"region": "East", "product": "Gadget", "amount": 150},
    {"region": "West", "product": "Widget", "amount": 90},
]

print(dict_groupby(sales))