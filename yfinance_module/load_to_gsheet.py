'''
step 4: load data into final destination --> personal gsheet 
'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build


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
