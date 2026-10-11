def dict_groupby(data):

    result = {}

    for row in data:
        k = (row["region"], row["product"])
        result[k] = result.get(k, 0) + row["amount"]

    return result

sales = [
    {"region": "West", "product": "Widget", "amount": 120},
    {"region": "East", "product": "Widget", "amount": 85},
    {"region": "West", "product": "Gadget", "amount": 200},
    {"region": "East", "product": "Gadget", "amount": 150},
    {"region": "West", "product": "Widget", "amount": 90},
]

print(dict_groupby(sales))