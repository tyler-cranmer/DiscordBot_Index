import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import json

scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive.file',
'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("googleSheets.json", scope) #access the json key you downloaded earlier 
client = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = client.open("discordTests")  #opens discordTests google sheets
sheet1 = sheet.worksheet("Sheet1") #access Sheet1
masterSheetDB = sheet.worksheet("MSbd") #access masterSheetDB
masterSheetPeople = sheet.worksheet("MSpeople")

# sheet = sheet.sheet_name  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

ranges = ['A3:F8']
user_data = sheet1.batch_get(ranges)


#create a new list of lists,  
bd_data = []
product_data = []
treasury_data = []
creative_data = []
engineering_data = []
growth_data = []
expenses_data = []
mvi_data = []
analytics_data = []
peopleOrgCom_data = []
InstBusiness_data = []
metaGov_data = []
other_data = []

bdCount = 0
peopleCount = 0
for lists in user_data: #loops through the data 
    for contribution in lists:
        for groupId in contribution:
            if groupId == 'BD':
                bd_data.append(contribution)
                bdCount+=1
            elif groupId == 'People Org & Community':
                peopleOrgCom_data.append(contribution)
                peopleCount +=1

nextLine = 4 + bdCount
masterSheetDB.batch_update([{
    'range': f'A{nextLine}',
    'values': bd_data,
}])

nextLines = 4 + peopleCount
masterSheetPeople.batch_update([{
    'range': f'A{nextLines}',
    'values': peopleOrgCom_data,
}])


pprint(len(bd_data))
pprint(len(peopleOrgCom_data))