import gspread
from oauth2client.service_account import ServiceAccountCredentials

class UserSheet:
    def __init__(self,owlID,sheetName,worksheetName):
        self.owlID = owlID
        self.sheetName = sheetName
        self.worksheetName = worksheetName
        self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
            ]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name("sheetCreds.json", self.scope) #access the json key you downloaded earlier 
        self.client = gspread.authorize(self.credentials) # authenticate the JSON key with gspread
