import sys
def all_stocks():
    companies = {
        'Apple' : 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }
    stocks = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    if len(sys.argv) == 2:
        line = sys.argv[1]
        list_of_names = []
        name = ""
        for ch in line:
            if ch == ',':
                list_of_names.append(name.strip())
                name = ""
            else:
                name += ch
        list_of_names.append(name.strip())
        if '' not in list_of_names:
            for text in list_of_names:
                if (text.lower()).capitalize() in companies.keys():
                    print((text.lower()).capitalize()," stock price is ",stocks[companies[(text.lower()).capitalize()]])
                elif text.upper() in companies.values():
                    cmp = ""
                    for comp in companies.keys():
                        if companies[comp] == text.upper():
                            cmp = comp
                    print(f"{(text.upper())} is a ticker symbol for {(cmp.lower()).capitalize()}")
                else:
                    print(f"{(text.lower()).capitalize()} is an unknown company or an unknown ticker symbol")
if __name__ == '__main__':
    all_stocks()
