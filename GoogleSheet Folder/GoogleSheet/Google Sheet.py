from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# File path to your service account JSON key
SERVICE_ACCOUNT_FILE = 'C:\\Users\\Dejan\\PycharmProjects\\GoogleSheet\\scraping-443109-b200d6923dfc.json '

# Scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Authenticate and initialize service
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

# Define your Google Sheet ID (from the URL)
SPREADSHEET_ID = '1rQmmNW7T2sukDcXNw9n4vRvBuh66Mn7q_JS3pDj_RJ8'

# Read data from the sheet
def read_sheet():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Blad1!A1:AY12").execute()
    return result.get('values', [])

# Write data to the sheet
def write_sheet():
    sheet = service.spreadsheets()
    values = [["Name", "Email"], ["John Doe", "john@example.com"]]
    body = {"values": values}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Blad1!A1",
        valueInputOption="RAW",
        body=body
    ).execute()
    return result

# Example usage
print("Reading from the sheet...")
print(read_sheet())

print("Writing to the sheet...")
print(write_sheet())
