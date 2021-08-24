import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import sqlite3
from database import AddContributor, AddContribution
import datetime

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
userInfoSheet = sheet.worksheet("Sheet2")
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


functionalGroupSheets = [businessDevSheet, productSheet, treasurySheet, creativeSheet, developmentSheet, growthSheet, expenseSheet, mviSheet, analyticsSheet, peopleOrgSheet, intBusinessSheet, metaGovSheet, otherSheet]



def collectContributorSheet(worksheetName): #collects info from sheets and puts it in SingleContributor TABLE
    db = 'index_contribution.db'
    ranges = ['A3:F51']
    user_data = worksheetName.batch_get(ranges)

    date = datetime.datetime.now()

    for outershell in user_data:
        for innershell in outershell:
            if len(innershell) > 2 and (innershell[5] == 'BD' or 'Product' or 'Treasury' or 'Creative & Design' or 'Dev/Engineering' or 'Growth' or 'Expenses' or 'MVI' or 'Analytics' or 'People Org & Community' or 'Institutional Business' or 'MetaGov' or 'Other'):
                    AddContribution(db, date.strftime("%m/%y"), innershell[0], innershell[1], innershell[2], innershell[3], innershell[4], innershell[5])



def collectAllOwlIDs(): #collects all the users stored in Sheet2 of Owls and puts them into Contributor TABLE
    db = 'index_contribution.db'
    range = ['A2:C136']
    userInfoD = userInfoSheet.batch_get(range)

    for outershell in userInfoD:
        for innershell in outershell:
           AddContributor(db, innershell[0], innershell[1], innershell[2])


#Updates each Working Groups Mastersheet with the contributors data.
#NEED TO TAKE IN MM/YY to specify what month they want to look at. 
def updateMasterSheet(dbname):
    connection = sqlite3.connect(dbname)
    c = connection.cursor() 

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
    functionalAreas = [bd_data, product_data, treasury_data, creative_data, engineering_data, growth_data, expenses_data, mvi_data, analytics_data, peopleOrgCom_data, intBusiness_data, metaGov_data, other_data]

    c.execute("SELECT USER_ID, DISCORD_NAME, CONTRIBUTION_INFO, LINKS, OTHER_NOTES, FUNCTIONAL_GROUP FROM SINGLECONTRIBUTION WHERE DATE = '08/21'")
    l = list(c.fetchall())
    newlist = list(map(list, l))
   
    for lists in newlist:
        for contribution in lists:
            if contribution == 'BD':
                bd_data.append(lists)
            elif contribution == 'Product':
                product_data.append(lists)
            elif contribution == 'Treasury':
                treasury_data.append(lists)
            elif contribution == 'Creative & Design':
                creative_data.append(lists)
            elif contribution == 'Dev/Engineering':
                engineering_data.append(lists)
            elif contribution == 'Growth':
                growth_data.append(lists)
            elif contribution == 'Expenses':
                expenses_data.append(lists)
            elif contribution == 'MVI':
                mvi_data.append(lists)
            elif contribution == 'Analytics':
                analytics_data.append(lists)
            elif contribution == 'People Org & Community':
                peopleOrgCom_data.append(lists)
            elif contribution == 'Institutional Business':
                intBusiness_data.append(lists)
            elif contribution =='MetaGov':
                metaGov_data.append(lists)
            elif contribution == 'Other':
                other_data.append(lists)

    start = 4

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



#Clears last MasterSheet Data
def clearLastMonthsData():
    for list in functionalGroupSheets:
        list.batch_clear(["A4:V115"])
    print("Clearing Last months data is complete")




def main():
    # collectAllOwlIDs()
    # collectContributorSheet(contributionSheet2)
    # updateMasterSheet('index_contribution.db')
    # clearLastMonthsData()

if __name__ == '__main__':

    main()