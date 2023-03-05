'''
step 2: get the dividend amount declared for the past years 
'''

import pandas as pd
from div_eval import div_eval


def get_dividend(stock):
    dividend = round(stock.dividends, 3) # 3 decimal point
    data = pd.DataFrame(dividend)
    data = data.reset_index() # take care of the table  arrangement
    average = data["Dividends"].tail(10).mean() # average dividend for the past 10 years
    print(f"the annual average dividend for the past 10 years for {stock} is {average}")
    div_eval(average)

