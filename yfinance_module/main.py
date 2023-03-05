'''
Author: Jason
Creation Date: 05/03/2023

Referenced from:

https://www.youtube.com/watch?v=4ssigWmExak 

ETL flow:

main.py --> get_dividend (get the dividend amount) --> div_eval (carry out evaluation) --> load_to_gsheet
'''

import yfinance as yf
import pandas as pd

from get_dividend import get_dividend


def main():
    '''
    step 1: set up shares we want to evaluate:
    https://finance.yahoo.com/quote/5258.KL?p=5258.KL&.tsrc=fin-srch
    as a sample, bimb5258 will be used
    '''
    stock_id = "5258"
    stock = yf.Ticker(stock_id + '.KL') # search the stocks we want to evaluate
    dividend = get_dividend(stock)
    return dividend

if __name__ == "__main__":
    main()

