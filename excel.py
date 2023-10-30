from pprint import pprint
import requests
# from binance import p2p, market
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'key_admin.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1-mb5Eu72jKW8kWrwWnAr7BRrioE7OCVVEMUBI6SnPlg'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


def append_values(range_name, x, y, z):
    try:
        values = [
            [
                f"{x}", f"{y}", f"{z}"
            ],
        ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="USER_ENTERED", body=body).execute()
        # print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


# append_values("B4:D4", "1", 3, "5")










# def update_wallet(x, y):
#     values = service.spreadsheets().values().batchUpdate(
#     spreadsheetId=spreadsheet_id,
#     body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             # Different Bank
#             {"range": f"{x}",
#              "majorDimension": "COLUMNS",
#              "values": [[f"{y}"]]},
# 	]
#     }
#     ).execute()
