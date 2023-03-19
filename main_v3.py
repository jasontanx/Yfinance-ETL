'''
Author: Jason
Creation Date: 18/03/2023

Referenced from:

https://www.youtube.com/watch?v=4ssigWmExak 
'''

from datetime import date
import yfinance as yf
import pandas as pd
#import plotly.graph_objects as g
# import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

import requests
from bs4 import BeautifulSoup

'''
share code 5258 will be used as an example
BIMB Berhad (5258.KL)
https://finance.yahoo.com/quote/5258.KL?p=5258.KL&.tsrc=fin-srch
'''

def load_to_gsheet(df):
    '''
    load data into personal gsheet
    '''
    SERVICE_ACCOUNT_FILE = 'secret_key.json' # cred to allow that access

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"] # asking for access to the scope

    creds = None
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES) # creates actual credentials
    
    spreadsheet_id = '11yP1f4cpa-RHipRL6MQKpfXoXQsb1gkt0aSSbBZj1Us'

    service = build('sheets', 'v4', credentials=creds)

    # calling sheets API
    sheet = service.spreadsheets()
    values = df.reset_index().values.tolist()
    body = {
        'values': values,
    }
    result = sheet.values().append(spreadsheetId=spreadsheet_id,
                                    range="yfinance!A2", valueInputOption='USER_ENTERED', body=body).execute() # append() / update()

    print(f'{result.get("updatedCells")} cells updated.')



def convert_to_df(stock_id,cheap,middle,expensive):
    '''
    convert data into dataframe before ingesting into google sheet
    '''
    today = date.today().strftime('%Y-%m-%d')

    if stock_id == '5258':
        stock_name = 'BIMB'
    else:
        stock_name = 'NULL'

    # try:
    #     url = f"https://finance.yahoo.com/quote/{stock_id}.KL?p={stock_id}.KL&.tsrc=fin-srch"
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     #stock_name = soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text
    #     stock_name = soup.find('h1', {'class': 'D(ib) Fz(24px) Mb-10'}).find('span').text
    #     print(stock_name)

    # except Exception as e:
    #     print(f"Error getting stock name: {e}")
    #     stock_name = "Unknown"


    data_dict = {'cheap': cheap, 'middle': middle, 'expensive': expensive, 'date': today}
    df = pd.DataFrame([data_dict], index=[stock_name])
    load_to_gsheet(df)
    

def div_eval(average,stock_id):
    '''
    create a sets of rules set by us for dividend evaluation
    '''
    safe = 0.8 # 20% margin of error --> safe boundary (margin of safety 安全边际)

    cheap = round(average * 15 * safe, 2) # years took to return on investment --> 15
    middle = round(average * 20 * safe, 2) # '2' refers to the decimal points
    expensive = round(average * 25 * safe, 2) # 25 years ROI

    print(f"cheap: {cheap}")
    print(f"middle: {middle}")
    print(f"expensive: {expensive}")
    convert_to_df(stock_id,cheap,middle,expensive)


def dividend(stock, stock_id):
    '''
    get dividend information
    '''
    dividend = round(stock.dividends, 3) # 3 decimal point
    data = pd.DataFrame(dividend)
    data = data.reset_index() # take care of the table  arrangement
    average = data["Dividends"].tail(10).mean() # average dividend for the past 10 years
    print(average)
    div_eval(average, stock_id)

def main():
    '''
    step 1: set up shares we want to evaluate:
    https://finance.yahoo.com/quote/5258.KL?p=5258.KL&.tsrc=fin-srch
    as a sample, bimb5258 will be used
    '''
    stock_id = "5258" 
    stock = yf.Ticker(stock_id + '.KL') # search the stocks we want to evaluate
    dividend(stock, stock_id)


if __name__ == "__main__":
    main()


