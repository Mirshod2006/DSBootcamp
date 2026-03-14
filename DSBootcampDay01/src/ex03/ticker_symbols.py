import sys

def stock_prices():
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
        if (sys.argv[1].lower()).upper() in companies.values():
            cmp=""
            for company in companies.keys():
                if companies[company] == (sys.argv[1].lower()).upper():
                    cmp = company
            print(cmp," ",stocks[(sys.argv[1].lower()).upper()])

if __name__ == '__main__':
    stock_prices()