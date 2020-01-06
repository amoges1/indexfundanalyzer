from bs4 import BeautifulSoup
import requests
import time
import csv

# etf_index_stocks=['DDLS', 'FDVV', 'FTEC', 'IWV', 'SCHD', 'SPY', 'SPYD', 'VBR', 'VGT', 'VOO', 'VOOG', 'VOOV', 'VT', 'VTI', 'VXUS', 'VYM', 'VYMI', 'VWO', 'VNQ']
etf_index_bonds=['ANGL', 'BND', 'BSV', 'HYS', 'JNK', 'SJNK']
# etf_indexes_list=['DDLS', 'FDVV', 'FTEC', 'IWV', 'SCHD', 'SPY', 'SPYD', 'VBR', 'VGT', 'VOO', 'VOOG', 'VOOV', 'VT', 'VTI', 'VXUS', 'VYM', 'VYMI', 'VWO', 'VNQ']


class ETF:
    ''' ETF Class representing an index fund - collection of stocks '''
    def __init__(self, title, stocks):
        self.title = title
        self.stocks = []

    def getValues(self):
        return self.title, self.stocks

class Stock:
    ''' Stock Class representing a single stock and relative weight in ETF'''
    def __init__(self, title, weight):
        self.title = title
        self.weight = weight


def get_etf_holdings(etf_indexes_list):

    # create a dict
    etf_book = dict()

    for etf in etf_indexes_list:
        print("Now loading...{}".format(etf))
        # Retrieve list of top 15 stocks and their weights
        first15_url='https://etfdb.com/etf/{}/#etf-holdings&sort_name=weight&sort_order=desc&page=1'.format(etf)
        # second15_url='https://etfdb.com/etf/{}/#etf-holdings&sort_name=weight&sort_order=desc&page=2'.format(etf)

        first15stock_names = BeautifulSoup(requests.get(first15_url).text, 'html.parser').find_all('td', {'data-th': 'Holding'})
        first15stock_weights = BeautifulSoup(requests.get(first15_url).text, 'html.parser').find_all('td', {'data-th': 'Weighting'})

        # Optional - Retrieve next 15 stocks due to pagination
        # second15stock_names = BeautifulSoup(requests.get(second15_url).text, 'html.parser').find_all('td', {'data-th': 'Holding'})
        # second15stock_weights = BeautifulSoup(requests.get(second15_url).text, 'html.parser').find_all('td', {'data-th': 'Weighting'})

        # Act normal!
        time.sleep(25) 
        
        # Optional - Combine first 15 + second 15 stocks
        # Combine lists of stocks and their weights
        # first15stock_names.append(second15stock_names)
        # first15stock_weights.append(second15stock_weights)
        
        # Clean information from web scrape above
        clean_stock_names = [ stock.getText() for stock in first15stock_names]
        clean_stock_weights = [ float(weight.getText()[:-1]) for weight in first15stock_weights]
        clean_stock_dict = dict(zip(clean_stock_names, clean_stock_weights))
      
        # Track stock/weight in master dict
        for stock in clean_stock_dict:
            print("Calculating...{}".format(stock))
            if stock not in etf_book:
                etf_book[stock] = clean_stock_dict[stock]
            else:
                etf_book[stock] += clean_stock_dict[stock]

    # write to csv 
    with open('etf_indexes_breakdown.csv', mode='w') as etf_indexes_breakdown:
        writer = csv.writer(etf_indexes_breakdown, delimiter=',')
        for stock in etf_book:
            writer.writerow([stock, etf_book[stock]])
        
        

get_etf_holdings(etf_index_bonds)

#soup.find_all([['td', {'data-th':'Holding'}], ['td', {'data-td': 'Weighting'}]])
