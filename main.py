'''
Author: Jason
Creation Date: 04/03/2023


jason2022@myfirstproject-364809.iam.gserviceaccount.com
'''

import yfinance as yf
import pandas as pd
#import plotly.graph_objects as g
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

'''
share code 1023 will be used as an example
CIMB Group Holdings Bhd (1023.KL)
https://finance.yahoo.com/quote/1023.KL?p=1023.KL&.tsrc=fin-srch 
'''

def load_to_gsheet(df):
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
    result = sheet.values().update(spreadsheetId=spreadsheet_id,
                                    range="yfinance!A1", valueInputOption='USER_ENTERED', body=body).execute() # append

    print(f'{result.get("updatedCells")} cells updated.')



def convert_to_df(cheap,middle,expensive):
    data_dict = {'cheap': cheap, 'middle': middle, 'expensive': expensive}
    df = pd.DataFrame.from_dict(data_dict, orient='index', columns =['values'])
    load_to_gsheet(df)
    

def div_eval(average):
    safe = 0.8 # 20% margin of error --> safe boundary (margin of safety 安全边际)

    cheap = round(average * 15 * safe, 2) # years took to return on investment --> 15
    middle = round(average * 20 * safe, 2) # '2' refers to the decimal points
    expensive = round(average * 25 * safe, 2) # 25 years ROI

    print(f"cheap: {cheap}")
    print(f"middle: {middle}")
    print(f"expensive: {expensive}")
    convert_to_df(cheap,middle,expensive)


def dividend(stock):
    dividend = round(stock.dividends, 3) # 3 decimal point
    data = pd.DataFrame(dividend)
    data = data.reset_index() # take care of the table  arrangement
    average = data["Dividends"].tail(10).mean() # average dividend for the past 10 years
    print(average)
    div_eval(average)

def main():
    '''
    step 1: set up shares we want to evaluate:
    https://finance.yahoo.com/quote/5258.KL?p=5258.KL&.tsrc=fin-srch
    as a sample, bimb5258 will be used
    '''
    stock_id = "5258"
    stock = yf.Ticker(stock_id + '.KL') # search the stocks we want to evaluate
    dividend(stock)

if __name__ == "__main__":
    main()


