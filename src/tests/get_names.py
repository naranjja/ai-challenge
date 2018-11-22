import json
x = json.loads(open(f"./../data/names.json", "r", encoding="utf-8").read())
print(list(x.keys()))