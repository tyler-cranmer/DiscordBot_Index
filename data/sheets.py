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







class UserSheet:
    def __init__(self, url):
        self.url = url
        # self.db = 'index_contribution.db'
        self.db = 'test.db'
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

        def date_sub(arg):                              #helper function to cover the people who submit on the 1st of the month and the rest of the stragglers. 
            date = int(arg.strftime("%d"))                #if the current day is within the first week of the month, it will return the previous month for the date. else, return current month
            if date <= 7:
                date = datetime.datetime.now().strftime("%m/%y")
                today_date = datetime.date.today()
                first = today_date.replace(day=1)
                lastMonth = first - datetime.timedelta(days=1)
                return(lastMonth.strftime("%m/%y"))
            else:
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
                if len(innershell) >= 8 and innershell[2] != '' and (innershell[6] == 'Community' or 'Growth' or 'Governance' or 'Finance' or 'Product') :
                    dash_list = list(map(is_empty, innershell))
                    DB.AddContribution(db, date_sub(datetime.datetime.now()), dash_list[0], dash_list[1], dash_list[2], dash_list[3], dash_list[4], dash_list[5], dash_list[6], dash_list[7], dash_list[8], dash_list[9])
                    print(f'{dash_list} \n {date_sub(datetime.datetime.now())}')
                    count+=1
  
        return count, rows



class NewUser:
    def __init__(self):
            # self.db = 'index_contribution.db'
            self.db = 'test.db'
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
        self.raw_input = sheet.get_worksheet_by_id(raw_input_creds) #connects with raw input sheet <----------NEED TO DELETE --------->
        self.finance_nest = sheet.get_worksheet_by_id(finance_nest_creds)
        self.growth_nest = sheet.get_worksheet_by_id(growth_nest_creds)
        self.community_nest = sheet.get_worksheet_by_id(community_nest_creds)
        self.product_nest = sheet.get_worksheet_by_id(product_nest_creds)
        self.governance_nest = sheet.get_worksheet_by_id(governance_nest_creds)
        self.owl_ids = sheet.get_worksheet_by_id(owl_sheet_creds) #connects with owl id reference worksheet

    # MIGHT TAKE THIS ENTIRE FUNCTION OUT> DONT REALLY NEED TO COLLECT OWLIDS. 
    #collects all the users info stored in Owl ID reference worksheet and puts them into Contributor TABLE
    def collectAllOwlIDs(self): 
        # db = 'index_contribution.db'
        db = 'test.db'
        range = ['A2:B250']
        userInfo = self.owl_ids.batch_get(range)

        for outershell in userInfo:
            for innershell in outershell:
                if innershell[0] != '':
                    DB.AddContributor(db, innershell[0], innershell[1])

    #change wallet address.    
    #They might want this to connect to google sheets database....    
    def changeWalletAddress(self, owlId, walletAddress): 
        # db = 'index_contribution.db'
        db = 'test.db'
        DB.changeWallet(db, owlId, walletAddress)



    def updateMasterSheet(self): #updates the mastersheet.
        # dbname = 'index_contribution.db'
        dbname = 'test.db'
        connection = sqlite3.connect(dbname)
        c = connection.cursor() 

        current_month = datetime.datetime.now().strftime("%m/%y")
        today_date = datetime.date.today()
        first = today_date.replace(day=1)
        last_month = first - datetime.timedelta(days=1)

        c.execute("SELECT OWL_ID, DISCORD_NAME, CONTRIBUTION_INFO, HAS_DISCUSSED, LINKS, OTHER_NOTES, HOURS, NEST, POD, LEAD_TO_REVIEW FROM SINGLECONTRIBUTION WHERE DATE = ?", (current_month,))   #for testing purposes     
        # c.execute("SELECT OWL_ID, DISCORD_NAME, CONTRIBUTION_INFO, HAS_DISCUSSED, LINKS, OTHER_NOTES, HOURS, NEST, POD, LEAD_TO_REVIEW FROM SINGLECONTRIBUTION WHERE DATE = ?", (last_month.strftime("%m/%y"),))
        l = list(c.fetchall())
        l2 = list(map(list, l)) #holds all the contribution data for the month

        row_id = 4 # row 4-108 is reserved for main contributors. 

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

       
            new_data = sorted(data)
            for x in range(len(new_data)):
                if new_data[x][0] < 10:
                    new_data[x][0] = str(new_data[x][0])
                    new_data[x][0] = '#00' + new_data[x][0] 
                elif new_data[x][0] < 100:
                    new_data[x][0] = str(new_data[x][0])
                    new_data[x][0] = '#0' + new_data[x][0]
                elif new_data[x][0] < 1000:
                    new_data[x][0] = str(new_data[x][0])
                    new_data[x][0] = '#' + new_data[x][0]
            return new_data

        #inserts titles for all each contributor
        def insert_title(owl_id,row_id):
            title_data = [owl_id, f"=VLOOKUP(A{row_id},'Owl ID reference'!$A$2:$B$600,2,FALSE)", 'Contribution', 'Has this contribution been discussed with your WGL?','Link to Work', 'Other notes', 'Time contributed (Hours)', '# Functional area', 'Nominated WGL to review' ,'Product',
            f'=sumifs($K$3:$K$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"F.Nest")', f'=sumifs($L$3:$L$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Product")', f'=sumifs(M$3:M$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"BD")',
            f'=sumifs($N$3:$N$1000,$B$3:B$1000,B{row_id},$H$3:$H$1000,"Creative & Design")', f'=sumifs($O$3:$O$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Dev/Engineering")', f'=sumifs($P$3:$P$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Growth&Marketing")',
            f'=sumifs($Q$3:$Q$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Expenses")', f'=sumifs($R$3:$R$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"MVI")', f'=sumifs($S$3:$S$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Analytics")',
            f'=sumifs($T$3:$T$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Institutional Business")', f'=sumifs($U$3:$U$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Talent, Ops & Change")', f'=sumifs($V$3:$V$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"MetaGov")',
            f'=sumifs($W$3:$W$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Other")', f'=sumifs($X$3:$X$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Lang-Ops")',f'=sumifs($Y$3:$Y$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Asia Pacific")',
            f'=sumifs($Z$3:$Z$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Woman+Non-Binary")', f'=sumifs($AA$3:$AA$1000,$B$3:$B$1000,B{row_id},$H$3:$H$1000,"Governance")', f'=sum(K{row_id}:AA{row_id})+AC{row_id + 1}', '', '', '',f'=(AB{row_id}/$B$1)+AD{row_id + 1}',
            f'=AE{row_id + 1}']

            ## WXY AC fixed USDC Stipen
            #need to fix data array and update 

            self.raw_input.insert_row(title_data, index = row_id, value_input_option='USER_ENTERED')


            #Format the first A-B Cells
            self.raw_input.format(f'A{row_id}:B{row_id}', {
                "backgroundColor": {
                "red": 1.0,
                "green": 0.0,
                "blue": 0.0
                },
                "horizontalAlignment": "CENTER",
                "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 1.0
                },
                "fontSize": 12,
                "bold": True
                }
            })
            #Format for C-H cells
            self.raw_input.format(f'C{row_id}:J{row_id}', {
                    "backgroundColor": {
                    "red": 0.15,
                    "green": 0.0,
                    "blue": 0.50
                    },
                    "horizontalAlignment": "CENTER",
                    "textFormat": {
                    "foregroundColor": {
                        "red": 1.0,
                        "green": 1.0,
                        "blue": 1.0
                    },
                    "fontSize": 12,
                    "bold": True
                    }
            }) 
            #Format for I-Z cells
            self.raw_input.format(f'K{row_id}:AH{row_id}', {
                "backgroundColor": {
                "red": 0.15,
                "green": 0.0,
                "blue": 0.50
                },
                "horizontalAlignment": "CENTER",
                "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 1.0
                },
                "fontSize": 10,
                "bold": False
                }
            })

        newlist = sort_list(l2)


       #Batch updates contribution list
        self.raw_input.batch_update([{
           'range': f'A{row_id}',
            'values': newlist, 
        }])
        

        # creates the list of lists for columns Total($) and Total(Index) formulas 
        # this allows for a batch_update. 
        dollar_sum = []
        index_sum= []
        for x in range(len(newlist)):
            dollar_sum.append(f'=SUM(K{row_id+x}:AA{row_id+x})')
            index_sum.append(f'=(AB{row_id+x}/$B$1)')

        dollar_sum_l = [[x] for x in dollar_sum]
        index_sum_l = [[x] for x in index_sum]

        #batch update all forumlas to master sheet
        #rowId hard coded here
        self.raw_input.batch_update([{
           'range': 'AB4',
            'values': dollar_sum_l, 
        }, {'range': 'AF4',
            'values': index_sum_l,
            }], value_input_option = 'USER_ENTERED')


        ##### creates the titles for each person #######
        first_owl = ['holder'] #used as a starting point
        title_row_id = 4 #was 109  
        for x in range(len(newlist)):
            ids = newlist[x][0]
            if ids != first_owl:
                first_owl = ids
                insert_title(first_owl, title_row_id)
                title_row_id +=2
            else:
                title_row_id +=1
        
    


    #Clears last MasterSheet Data
    #Resets sheet format
    def clearLastMonthsData(self):
        range = ['A4:AH1500']
        self.raw_input.format('A4:AH1500', {
            "backgroundColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
            }, 
            "horizontalAlignment": "CENTER",
            "textFormat": {
            "foregroundColor": {
                "red": 0.0,
                "green": 0.0,
                "blue": 0.0
            },
                "fontSize": 10,
                "bold": False
            } 
        })
        self.raw_input.batch_clear(range)


