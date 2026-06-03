import requests

waluty = {
    "eur": "Euro",
    "usd": "Dolar Amerykański",
    "czk": "Korona czeska",
    "sbd": "Dolar Wysp Salomona",

    "sek": "Korona szwedzka",
    "lkr": "Rupia lankijska",
    "jpy": "Jen",
    "pen": "Sol peruwiański"
}

kursy = {
    "eur": 0,
    "usd": 0,
    "czk": 0,
    "sbd": 0,

    "sek": 0,
    "lkr": 0,
    "jpy": 0,
    "pen": 0
}

test = requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/pln.json')
json = test.json()

for waluta in waluty:
    kursy[waluta] = json["pln"][waluta]
    print(kursy[waluta])
print(json["pln"]["usd"])

#with open("test.txt","w") as f:
#    f.write(json)
