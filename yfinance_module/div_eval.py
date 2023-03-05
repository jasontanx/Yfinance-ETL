'''
step 3: carry out the evaluation on the stock

Point 1: 
Dividend Discount Model (DDM) -->
DDM is a valuation method used to estimate the intrinsic value of a company's 
stock based on the present value of its expected future dividends

Point 2:
Allow us to know many years will it take for investor to break-even based on 
the stock price purchased

Point 3:
Set margin of safety --> 
Based on the concept introduced by Benjamin Graham

'''
from prefect import task, flow
import pandas as pd
from load_to_gsheet import load_to_gsheet


def div_eval(average):
    safe = 0.8 # 20% margin of error --> safe boundary (margin of safety 安全边际)
    
    # '2' refers to the decimal points
    cheap = round(average * 15 * safe, 2) # years took to return on investment (ROI) --> 15 years
    middle = round(average * 20 * safe, 2) # ROI --> 20 years 
    expensive = round(average * 25 * safe, 2) # ROI --> 25 years 

    print(f"cheap: {cheap}")
    print(f"middle: {middle}")
    print(f"expensive: {expensive}")
    convert_to_df(cheap,middle,expensive)



def convert_to_df(cheap,middle,expensive):
    data_dict = {'cheap': cheap, 'middle': middle, 'expensive': expensive}
    df = pd.DataFrame.from_dict(data_dict, orient='index', columns =['values'])
    load_to_gsheet(df)

