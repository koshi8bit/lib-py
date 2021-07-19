# https://habr.com/ru/post/483302/

from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os


class GoogleSheets:
    service = None
    spreadsheet_id = None

    def __init__(self, creds_json: str, spreadsheet_id: str):
        credentials_file = creds_json
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        http_auth = credentials.authorize(httplib2.Http())
        self.service = build('sheets', 'v4', http=http_auth)

        self.spreadsheet_id = spreadsheet_id

    def read(self, rangee):
        result_input = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                                range=rangee).execute()
        values_input = result_input.get('values', [])
        return values_input

    def write(self, rangee, data):
        res = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=rangee, valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS", body={"values": data}
        ).execute()

        is_ok = isinstance(res, dict) and 'spreadsheetId' in res and res['spreadsheetId'] == self.spreadsheet_id

        if not is_ok:
            raise ValueError('error while writing to google sheet')

        return is_ok
