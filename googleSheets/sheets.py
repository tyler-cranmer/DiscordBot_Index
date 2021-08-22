import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import json


#https://collab-land.gitbook.io/collab-land/bots/discord
#https://wickbot.com/



scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive.file',
'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("sheetCreds.json", scope) #access the json key you downloaded earlier 
client = gspread.authorize(credentials) # authenticate the JSON key with gspread

sheet = client.open("discordTests")  #opens discordTests google sheets
contributionSheet1 = sheet.worksheet("Person1")
contributionSheet2 = sheet.worksheet("Person2")
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


# sheet = sheet.sheet_name  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

ranges = ['A3:F51']
user_data = contributionSheet1.batch_get(ranges)


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
intBusiness_data = []
metaGov_data = []
other_data = []


global bdCount
global productCount 
global treasuryCount 
global creativeCount 
global engineeringCount 
global growthCount
global expensesCount 
global mviCount
global analyticsCount
global peopleCount
global instBusinessCount
global metaGovCount
global  otherCount

functionalAreas = [bd_data, product_data, treasury_data, creative_data, engineering_data, growth_data, expenses_data, mvi_data, analytics_data, peopleOrgCom_data, intBusiness_data, metaGov_data, other_data]

bdCount = 0
productCount = 0
treasuryCount = 0
creativeCount = 0
engineeringCount = 0
growthCount = 0
expensesCount = 0
mviCount = 0
analyticsCount= 0
peopleCount = 0
instBusinessCount = 0
metaGovCount = 0
otherCount = 0

for lists in user_data: #loops through the data 
    for contribution in lists:
        for groupId in contribution:
            if groupId == 'BD':
                bd_data.append(contribution)
                bdCount +=1
            elif groupId == 'Product':
                product_data.append(contribution)
                productCount += 1
            elif groupId == 'Treasury':
                treasury_data.append(contribution)
                treasuryCount +=1
            elif groupId == 'Creative & Design':
                creative_data.append(contribution)
                creativeCount +=1
            elif groupId == 'Dev/Engineering':
                engineering_data.append(contribution)
                engineeringCount +=1
            elif groupId == 'Growth':
                growth_data.append(contribution)
                growthCount +=1
            elif groupId == 'Expenses':
                expenses_data.append(contribution)
                expensesCount +=1
            elif groupId == 'MVI':
                mvi_data.append(contribution)
                mviCount +=1
            elif groupId == 'Analytics':
                analytics_data.append(contribution)
                analyticsCount +=1
            elif groupId == 'People Org & Community':
                peopleOrgCom_data.append(contribution)
                peopleCount +=1
            elif groupId == 'Institutional Business':
                intBusiness_data.append(contribution)
                instBusinessCount +=1
            elif groupId =='MetaGov':
                metaGov_data.append(contribution)
                metaGovCount +=1
            elif groupId == 'Other':
                other_data.append(contribution)
                otherCount +=1


functionalCountList = [bdCount, productCount, treasuryCount, creativeCount, engineeringCount, growthCount, expensesCount, mviCount, analyticsCount, peopleCount, instBusinessCount, metaGovCount, otherCount]
functionalDataList = [bd_data, product_data, treasury_data, creative_data, engineering_data, growth_data, expenses_data, mvi_data, analytics_data, peopleOrgCom_data, intBusiness_data, metaGov_data, other_data]

#Updates each Working Groups Mastersheet with the contributors data.

start = 4
nextLine = 0

businessDevSheet.batch_update([{
    'range': f'A{start}',
    'values': bd_data,
}])

productSheet.batch_update([{
    'range': f'A{start}',
    'values': product_data,
}])

treasurySheet.batch_update([{
    'range': f'A{start}',
    'values': treasury_data,
}])

creativeSheet.batch_update([{
    'range': f'A{start}',
    'values': creative_data,
}])

developmentSheet.batch_update([{
    'range': f'A{start}',
    'values': engineering_data,
}])

growthSheet.batch_update([{
    'range': f'A{start}',
    'values': growth_data,
}])

expenseSheet.batch_update([{
    'range': f'A{start}',
    'values': expenses_data,
}])

mviSheet.batch_update([{
    'range': f'A{start}',
    'values': mvi_data,
}])

analyticsSheet.batch_update([{
    'range': f'A{start}',
    'values': analytics_data,
}])

peopleOrgSheet.batch_update([{
    'range': f'A{start}',
    'values': peopleOrgCom_data,
}])

intBusinessSheet.batch_update([{
    'range': f'A{start}',
    'values': intBusiness_data,
}])

metaGovSheet.batch_update([{
    'range': f'A{start}',
    'values': metaGov_data,
}])

otherSheet.batch_update([{
    'range': f'A{start}',
    'values': other_data,
}])

print(" Updated Master Sheets Complete")

##################################################################################################################
