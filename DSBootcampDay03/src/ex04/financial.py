from bs4 import BeautifulSoup
import requests
import sys
import time
import pstats
import cProfile

def fetch_data(ticker,field):
    if ticker.isnumeric():
        raise Exception("Please make sure, you are entering valid comnpany ticker!")
    url = f'https://finance.yahoo.com/quote/{ticker.upper()}/financials/?p={ticker.lower()}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        raise Exception("According to given data, web-site could be found!")
    data = BeautifulSoup(response.text,'html.parser')
    tableBody = data.find('div',{'class':'tableBody'})
    if not tableBody:
        raise Exception("Financial data is not available!")
    rows_data = tableBody.find_all('div',{'class':'row'})
    searched_data = []
    for row in rows_data:
        row_title = row.find('div',{'class':'rowTitle'})
        if row_title and row_title.get_text().strip().lower() == field.lower():
            columns = row.find_all('div',{'class':'column'})
            searched_data = [col.get_text().strip() for col in columns]
            
            if data:
                # time.sleep(5)
                return tuple(searched_data)
    raise Exception("Please make sure, entered field exsists!")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('python3 financial.py <ticker_name> <field_name>')
        exit(1)
    try:
        profile = cProfile.Profile()
        profile.enable()
        print(fetch_data(sys.argv[1],sys.argv[2]))
        profile.disable()
        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.CUMULATIVE)

        with open('pstats-cumulative.txt','w') as file:
            results.stream = file
            results.print_stats(5)
    except Exception as e:
        print(str(e))