def read_records():
    return [
        {"id": 1, "region": "west", "amount": "120"},
        {"id": 2, "region": "east", "amount": "85"},
        {"id": 3, "region": "west", "amount": "bad"},
        {"id": 4, "region": "north", "amount": "200"},
        {"id": 5, "region": "east", "amount": None},
        
    ]

def write_records(records):
    for r in records:
        print(r)
