import json

with open("utils\\resources\\EZTV_RFERENCE_DICTIONARY.json") as titlesOb:
    data = json.load(titlesOb)
    titles = [k.replace("-", " ").title() for k,v in data.items()]

    print(titles[:10])