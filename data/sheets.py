import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
from data.database import DB
import datetime
import json
import time



with open("./config.json") as f:
    configData = json.load(f)

template_creds = configData["CONTRIBUTOR_SHEET_KEY"] #file_id for the new-contributor rewards sheet
master_creds = configData["MASTER_SHEET_KEY"]
owl_sheet_creds = configData['MASTER_OWLID_GID']
finance_nest_creds = configData['FINANCE_NEST_GID']
growth_nest_creds = configData['GROWTH_NEST_GID']
community_nest_creds = configData['COMMUNITY_NEST_GID']
product_nest_creds = configData['PRODUCT_NEST_GID']
governance_nest_creds = configData['GOVERNANCE_NEST_GID']
db_name = configData["database_name"]







class UserSheet:
    def __init__(self, url):
        self.url = url
        self.db = "index_db"
        self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
            ]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name("gSheetCreds.json", self.scope) #access the json key you downloaded earlier 
        self.client = gspread.authorize(self.credentials) # authenticate the JSON key with gspread


    #collects info from sheets and puts it in SingleContributor TABLE
    def collectContributorSheet(self): 
        sheet = self.client.open_by_url(str(self.url))
        contributionSheet = sheet.get_worksheet(1)
        ranges = ['A3:J51']
        user_data = contributionSheet.batch_get(ranges)
        db = self.db

        def date_sub(arg):     #We changed the submission dates, no longer need to account for laggers.            
            return arg.strftime("%m/%y")

        # function to check if a google sheet cell is empty.
        # fills empty cell with --- 
        def is_empty(x):
            if x == '':
                return '---'
            else:
                return x

        count = 0
        row = 2
        rows = []
        for outershell in user_data:  # Checks to make sure peoples Owl_Id column is formatted correctly.
            for innershell in outershell:
                row +=1  
                if len(innershell) >= 8 and not (innershell[0].startswith("#0") or innershell[0].startswith("#1") or innershell[0].startswith("#2")  # Checks to make sure peoples Owl_Id column is formatted correctly.
                or innershell[0].startswith("#3") or innershell[0].startswith("#4") or innershell[0].startswith("#5") 
                or innershell[0].startswith("#6") or innershell[0].startswith("#7") or innershell[0].startswith("#8") 
                or innershell[0].startswith("#9")): 
                    rows.append(row)
                    return count, rows
                    break

        for outershell in user_data:
            for innershell in outershell:            
                if len(innershell) >= 8 and innershell[2] != '' and (innershell[7] == 'Community' or 'Growth' or 'Governance' or 'Finance' or 'Product') :
                    dash_list = list(map(is_empty, innershell))
                    DB.AddContribution(db, date_sub(datetime.datetime.now()), dash_list[0], dash_list[1], dash_list[2], dash_list[3], dash_list[4], dash_list[5], dash_list[6], dash_list[7], dash_list[8], dash_list[9])
                    print(f'{dash_list} \n {date_sub(datetime.datetime.now())}')
                    count+=1
  
        return count, rows



class NewUser:
    def __init__(self):
            self.db = db_name
            self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
            ]
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name("gSheetCreds.json", self.scope) #access the json key you downloaded earlier 
            self.client = gspread.authorize(self.credentials) # authenticate the JSON key with gspread


    def create_spread_sheet(self):          
        contributor_sheet = self.client.open_by_key(template_creds)
        return contributor_sheet.url




class MasterControls:
    def __init__(self):
        scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name("gSheetCreds.json", scope) #access the json key you downloaded earlier 
        client = gspread.authorize(credentials) # authenticate the JSON key with gspread

        sheet = client.open_by_key(master_creds)  #connects with mastersheet
        self.finance_nest = sheet.get_worksheet_by_id(finance_nest_creds)
        self.growth_nest = sheet.get_worksheet_by_id(growth_nest_creds)
        self.community_nest = sheet.get_worksheet_by_id(community_nest_creds)
        self.product_nest = sheet.get_worksheet_by_id(product_nest_creds)
        self.governance_nest = sheet.get_worksheet_by_id(governance_nest_creds)

    # MIGHT TAKE THIS ENTIRE FUNCTION OUT> DONT REALLY NEED TO COLLECT OWLIDS. 
    #collects all the users info stored in Owl ID reference worksheet and puts them into Contributor TABLE
    def collectAllOwlIDs(self): 
        db = db_name
        range = ['A2:B250']
        userInfo = self.owl_ids.batch_get(range)

        for outershell in userInfo:
            for innershell in outershell:
                if innershell[0] != '':
                    DB.AddContributor(db, innershell[0], innershell[1])

    #change wallet address.    
    #They might want this to connect to google sheets database....    
    def changeWalletAddress(self, owlId, walletAddress): 
        db = db_name
        DB.changeWallet(db, owlId, walletAddress)



    def updateMasterSheet(self): #updates the mastersheet.
        dbname = db_name
        connection = sqlite3.connect(dbname)
        c = connection.cursor() 
        finance_list = []
        growth_list = []
        community_list = []
        product_list = []
        governance_list = []

        current_month = datetime.datetime.now().strftime("%m/%y")
        today_date = datetime.date.today()
        first = today_date.replace(day=1)
        last_month = first - datetime.timedelta(days=1)

        c.execute("SELECT OWL_ID, DISCORD_NAME, CONTRIBUTION_INFO, HAS_DISCUSSED, LINKS, OTHER_NOTES, HOURS, NEST, POD, LEAD_TO_REVIEW FROM SINGLECONTRIBUTION WHERE DATE = ?", (current_month,))   #for testing purposes     
        # c.execute("SELECT OWL_ID, DISCORD_NAME, CONTRIBUTION_INFO, HAS_DISCUSSED, LINKS, OTHER_NOTES, HOURS, NEST, POD, LEAD_TO_REVIEW FROM SINGLECONTRIBUTION WHERE DATE = ?", (last_month.strftime("%m/%y"),))
        db_list = list(c.fetchall())
        formatted_db_list = list(map(list, db_list)) #converts to a list of list. Formatting for gspread. 
 

        #transforms the the owl id into integers to allow for to sort all the contributions.
        # This was made because some people forget to submit all data at once, this allows for the master sheet to have continuity between all contributors. 
        def sort_list(data):
            for x in range(len(data)):
                if data[x][0][0:3] == '#00':
                    data[x][0] = int(data[x][0][3:4])
                elif data[x][0][0:2] == '#0':
                    data[x][0] = int(data[x][0][2:4])
                elif data[x][0][0:1] == '#':
                    data[x][0] = int(data[x][0][1:4])

            
            sorted_data = sorted(data) #simple sort of data
            for x in range(len(sorted_data)):
                if sorted_data[x][0] < 10:
                    sorted_data[x][0] = str(sorted_data[x][0])
                    sorted_data[x][0] = '#00' + sorted_data[x][0] 
                elif sorted_data[x][0] < 100:
                    sorted_data[x][0] = str(sorted_data[x][0])
                    sorted_data[x][0] = '#0' + sorted_data[x][0]
                elif sorted_data[x][0] < 1000:
                    sorted_data[x][0] = str(sorted_data[x][0])
                    sorted_data[x][0] = '#' + sorted_data[x][0]
            return sorted_data

        sorted_db_list = sort_list(formatted_db_list)

        # sort contributions by NEST working groups.
        for x in range(len(sorted_db_list)):
            if sorted_db_list[x][7] == 'Finance':
                finance_list.append(sorted_db_list[x])
            elif sorted_db_list[x][7] == 'Growth':
                growth_list.append(sorted_db_list[x])
            elif sorted_db_list[x][7] == 'Governance':
                governance_list.append(sorted_db_list[x])
            elif sorted_db_list[x][7] == 'Community':
                community_list.append(sorted_db_list[x])
            else:
                product_list.append(sorted_db_list[x]) 

       #Batch updates contribution list for Finance Nest
        row_id = 4
        self.finance_nest.batch_update([{
           'range': f'A{row_id}',
            'values': finance_list, 
        }])

        #Batch updates contribution list for Growth Nest
        self.growth_nest.batch_update([{
           'range': f'A{row_id}',
            'values': growth_list, 
        }])

        #Batch updates contribution list for Community Nest
        self.community_nest.batch_update([{
           'range': f'A{row_id}',
            'values': community_list, 
        }])

        #Batch updates contribution list for Product Nest
        self.product_nest.batch_update([{
           'range': f'A{row_id}',
            'values': product_list, 
        }])

        #Batch updates contribution list for Governance Nest
        self.governance_nest.batch_update([{
           'range': f'A{row_id}',
            'values': governance_list, 
        }])
    

    #Clears last MasterSheet Data
    #Resets sheet format
    def clearLastMonthsData(self):
        range = ['A4:J500']
        self.growth_nest.batch_clear(range)
        self.community_nest.batch_clear(range)
        self.product_nest.batch_clear(range)
        self.governance_nest.batch_clear(range)
        self.finance_nest.batch_clear(range)



