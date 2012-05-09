'''
Yahoo Finance CSV API
aking1012.com.my@pants.gmail.com
You can email me if you want,
but first you have to take off my pants.
'''

import os, urllib, datetime, csv
from types import ListType, StringType

def log(something):
    '''
    A logger function.
    I use it so I only have to change print ONE place on 2to3...
    or so I can switch to more robust logging.  Either way.
    '''
    print something

class YahooFinanceCsv():
    '''
    Convenience class for yahoo finance csv fetching
    '''
    def __init__(self):
        '''
        Get a list of symbols and make directories.
        I need to make this part OS agnostic.
        '''
        self.badkeys = []
        self.nasdaq_tickers = {}
        
        try:
            os.mkdir('/tmp/ycsvapi')
        except OSError, exce_os:
            exce_os = exce_os
        try:
            os.mkdir('/tmp/ycsvapi/csvcache')
        except OSError, exce_os:
            exce_os = exce_os
        try:
            os.mkdir('/tmp/ycsvapi/csvcache/historical')
        except OSError, exce_os:
            exce_os = exce_os
        try:
            os.mkdir('/tmp/ycsvapi/csvcache/today')
        except OSError, exce_os:
            exce_os = exce_os
        self.base_url_today = 'http://finance.yahoo.com/d/quotes.csv?s='
        self.base_url_historical = ''+\
            'http://ichart.finance.yahoo.com/table.csv?s='
        self.param_dict = {'Ask': 'a',
                      'Average Daily Volume': 'a2',
                      'Ask Size': 'a5',
                      'Bid': 'b',
                      'Ask RT': 'b2',
                      'Bid RT': 'b3',
                      'Book Value': 'b4',
                      'Bid Size': 'b6',
                      'Change and Percent Change': 'c',
                      'Change': 'c1',
                      'Commission': 'c3',
                      'Change RT': 'c6',
                      'After Hours Change RT': 'c8',
                      'Dividend per Share': 'd',
                      'Last Trade Date': 'd1',
                      'Trade Date': 'd2',
                      'Earnings per Share': 'e',
                      'Error Indication': 'e1',
                      'EPS Estimate Current Year': 'e7',
                      'EPS Estimate Next Year': 'e7',
                      'EPS Estimate Next Quarter': 'e7',
                      'Float Shares': 'f6',
                      'Day Low': 'g',
                      'Holdings Gain Percent': 'g1',
                      'Annualized Gain': 'g3',
                      'Holdings Gain': 'g4',
                      'Holdings Gain Percent RT': 'g5',
                      'Holdings Gain RT': 'g6',
                      'Day High': 'h',
                      'More info': 'i',
                      'Order book RT': 'i5',
                      '52 week low': 'j',
                      'Market Cap': 'j1',
                      'Market Cap RT': 'j3',
                      'EBITDA': 'j4',
                      'Change from 52 week low': 'j5',
                      'Percent change from 52 week low': 'j6',
                      '52 week high': 'k',
                      'Last Trade with time RT': 'k1',
                      'Change percent RT': 'k2',
                      'Last trade size': 'k3',
                      'Change from 52 week high': 'k4',
                      'Percent change from 52 week high': 'k4',
                      'Last Trade with time': 'l',
                      'Last Trade price': 'l1',
                      'High limit': 'l2',
                      'Low limit': 'l3',
                      'Day range': 'm',
                      'Day range RT': 'm2',
                      '50 day moving average': 'm3',
                      '200 day moving average': 'm4',
                      'Change from 200 day moving average': 'm5',
                      'Percent change from 200 day moving average': 'm6',
                      'Change from 50 day moving average': 'm7',
                      'Percent change from 50 day moving average': 'm8',
                      'Name': 'n',
                      'Notes': 'n4',
                      'Open': 'o',
                      'Previous close': 'p',
                      'Price paid': 'p1',
                      'Change in percent': 'p2',
                      'Price/Sales': 'p5',
                      'Price/Book': 'p6',
                      'Ex-Dividend Date': 'q',
                      'PE Ratio': 'r',
                      'Dividend pay date': 'r1',
                      'PE ratio': 'r2',
                      'PEG ratio': 'r5',
                      'Price/EPS Estimated Current Year': 'r6',
                      'Price/EPS Estimated Next Year': 'r7',
                      'Symbol': 's',
                      'Shares owned': 's1',
                      'Short ratio': 's7',
                      'Last trade time': 't1',
                      'Trade links': 't6',
                      'Ticker trend': 't7',
                      'One year target price': 't8',
                      'Volume': 'v',
                      'Holdings value': 'v1',
                      'Holding value RT': 'v7',
                      '52 week range': 'w',
                      'Day value change': 'w1',
                      'Day value change RT': 'w4',
                      'Stock exchange': 'x',
                      'Dividend yield': 'y',
                      'Not RT': '',
                      'RT': '',
                      'Historical defaults': 'ohgv',
                      'Candlestick RT': 'b2b3'
                      }
        self.ticker_data = {}
        self.fetch_symbol_list()
        self.symbols = self.nasdaq_tickers.keys()

    def set_symbols(self, symbols):
        '''
        Set the current symbols
        '''
        self.symbols = symbols

    def set_badkeys(self, keys=False):
        '''
        Set the badkeys
        '''
        if keys:
            for key in keys:
                if key not in self.badkeys:
                    self.badkeys.append(key)
        for key in self.badkeys:
            try:
                index = self.symbols.index(key)
                del self.symbols[index]
            except ValueError, error:
                error = error

    def clear_ticker_data(self):
        '''
        Obvious
        '''
        self.ticker_data = {}
        
    def fetch_symbol_list(self):
        '''
        Returns the symbol list
        '''
        csvfile = urllib.urlopen('http://www.nasdaq.com/'+\
                                 'screening/companies-by-name.aspx?'+\
                                 'letter=0&exchange=nasdaq&render=download')
        reader = csv.reader(csvfile, quotechar='"')
        for row in reader:
            self.nasdaq_tickers[row[0]] = {'Name': row[1],
                                           'LastSale': row[2],
                                           'MarketCap': row[3],
                                           'ADR TSO': row[4],
                                           'IPOyear': row[5],
                                           'Sector': row[6],
                                           'Subsector': row[7],
                                           'Summary': row[8]}

    def fetch_historical_single(self, symbol, date_component):
        '''
        For DRY
        '''
        url = self.base_url_historical + symbol + date_component
        urllib.urlretrieve(url, '/tmp/ycsvapi/csvcache/historical/'+\
                           symbol + ".csv")
    
    def fetch_historical_symbol_data(self, 
                                     symbol=False, 
                                     start_date=False,
                                     end_date=False):
        '''
        The start date and end date are time tuples.
        If you don't provide symbol it tries for all symbols fetched from the Nasdaq website.
        If you don't provide start_date it sets to the first day the Nasdaq was in operation.
        If you don't provide end_date it sets to today.
        '''
        
        #set up dates if they weren't provided
        if not start_date:
            #February 4, 1971 start date(first day NASDAQ market operated)
            start_date = datetime.date(1971, 4, 1).timetuple()
        if not end_date:
            #today
            end_date = datetime.datetime.today().timetuple()
        
        date_component = '&a='+str(start_date[1]-1)+\
                        '&b='+str(start_date[2]-1)+\
                        '&c='+str(start_date[0])+\
                        '&d='+str(end_date[1]-1)+\
                        '&e='+str(end_date[2]-1)+\
                        '&f='+str(end_date[0])+\
                        '&g=d'
        
        #get the data
        if type(symbol) is ListType:
            for a_symbol in symbol:
                self.fetch_historical_single(a_symbol, date_component)
        elif type(symbol) is StringType:
            self.fetch_historical_single(symbol, date_component)
        else:
            for the_symbol in self.symbols:
                self.fetch_historical_single(the_symbol,
                                             date_component)
        self.not_supported_symbols()

    def fetch_symbol_data_single(self, symbol, option_component):
        '''
        For DRY
        '''
        url = self.base_url_today + symbol + '&f=' + option_component
        urllib.urlretrieve(url, '/tmp/ycsvapi/csvcache/today/'+\
                           symbol+".csv")
        
    def fetch_symbol_data(self, symbol=False, params=False):
        '''
        Fetch symbol data.  The 'params' parameter should be a list of parameters you want to fetch.
        See the ones I have defined in self.param_dict.
        RT == Real-time, but I can't vouch for how real-time that means.
        The start date and end date are time tuples.
        '''
        
        #set up params
        fetch_these = ''
        if params:
            for param in params:
                try:
                    fetch_these += self.param_dict[param]
                except KeyError, excep_key:
                    log(str(excep_key) +\
                        ' Check YahooFinanceCsv.param_dict'+\
                        ' for supported parameters')
        else:
            log('You failed to provide parameters')
            return

        #get the data
        if type(symbol) is ListType:
            for a_symbol in symbol:
                self.fetch_symbol_data_single(a_symbol, fetch_these)
        elif type(symbol) is StringType:
            self.fetch_symbol_data_single(symbol, fetch_these)
        else:
            for the_symbol in self.symbols:
                self.fetch_symbol_data_single(the_symbol, fetch_these)
        self.not_supported_symbols()

    def not_supported_symbols(self):
        '''
        For removing unsupported symbols from the symbol list
        '''
        badkeys = []
        for a_symbol in self.symbols:
            try:
                with open('/tmp/ycsvapi/csvcache/historical/'+\
                          a_symbol+'.csv','r') as fil:
                    is_html = fil.readline()
                    if '<!doctype html public' in is_html:
                        badkeys.append(a_symbol)
            except IOError, error:
                error = error
                
        self.set_badkeys(badkeys)

if __name__ == "__main__":
    Y = YahooFinanceCsv()
    Y.fetch_symbol_list()
    Y.set_symbols(['MSFT', 'AAPL', 'ZZZZ'])
    Y.fetch_historical_symbol_data()
    Y.set_symbols(['MSFT', 'AAPL', 'YYYY'])
    Y.fetch_historical_symbol_data()
    log(str(Y.symbols))