import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive.file',
'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("sheetCreds.json", scope) #access the json key you downloaded earlier 
client = gspread.authorize(credentials) # authenticate the JSON key with gspread

sheet = client.open("discordTests")  #opens discordTests google sheets
masterSheet = sheet.worksheet("MasterSheet main") #access Sheet1
businessDevSheet = sheet.worksheet("BD")
productSheet = sheet.worksheet("Product")
treasurySheet = sheet.worksheet("Treasury")
creativeSheet = sheet.worksheet("Creative")
developmentSheet = sheet.worksheet("Dev")
growthSheet = sheet.worksheet("Growth")
expenseSheet = sheet.worksheet("Expense")
mviSheet = sheet.worksheet("MVI")
analyticsSheet = sheet.worksheet("Analytics")
peopleOrgSheet = sheet.worksheet("PeopleOrg")
intBusinessSheet =  sheet.worksheet("Int Business")
metaGovSheet = sheet.worksheet("MetaGov")
otherSheet = sheet.worksheet("Other")

functionalGroupSheets = [businessDevSheet, productSheet, treasurySheet, creativeSheet, developmentSheet, growthSheet, expenseSheet, mviSheet, analyticsSheet, peopleOrgSheet, intBusinessSheet, metaGovSheet, otherSheet]

def clearLastMonthsData():
    for list in functionalGroupSheets:
        list.batch_clear(["A4:V115"])
    print("Clearing Last months data is complete")

clearLastMonthsData()
print("Clearing Last months data is complete")