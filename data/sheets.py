import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
from data.database import DB
import datetime
import json
import time



with open("./config.json") as f:
    configData = json.load(f)

template_creds = configData["Contributor_key"] #file_id for the new-contributor rewards sheet
master_creds = configData["Master_key"]
owl_sheet_creds = configData['Master_owlID_id']
raw_input_creds = configData['Raw_input_id']




class UserSheet:
    def __init__(self, url):
        self.url = url
        self.db = 'index_contribution.db'
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
        contributionSheet = sheet.get_worksheet(0)
        ranges = ['A3:H51']
        user_data = contributionSheet.batch_get(ranges)
        db = self.db

        date = datetime.datetime.now()

        #function to check if a google sheet cell is empty.
        # fills empty cell with --- 
        def is_empty(x):
            if x == '':
                return '---'
            else:
                return x

        count = 0
        row = 2
        rows = []
        for outershell in user_data:
            for innershell in outershell:
                row +=1  
                if len(innershell) >= 7 and not (innershell[0].startswith("#0") or innershell[0].startswith("#2")  # Checks to make sure peoples Owl_Id column is formatted correctly.
                or innershell[0].startswith("#3") or innershell[0].startswith("#4") or innershell[0].startswith("#5") 
                or innershell[0].startswith("#6") or innershell[0].startswith("#7") or innershell[0].startswith("#8") 
                or innershell[0].startswith("#9")): 
                    rows.append(row)
                    return count, rows
                    break
                elif len(innershell) >= 7 and innershell[2] != '' and (innershell[6] == 'BD' or 'Product' or 'Treasury' or 'Creative & Design' or 'Dev/Engineering' or 'Growth' or 'Expenses' or 'MVI' or 'Analytics' or 'People Org & Community' or 'Institutional Business' or 'MetaGov' or 'Other' or 'Lang-Ops') :
        #             dash_list = list(map(is_empty, innershell))
        #             DB.AddContribution(db, date.strftime("%m/%y"), dash_list[0], dash_list[1], dash_list[2], dash_list[3], dash_list[4], dash_list[5], dash_list[6], dash_list[7])
        #             print(f'{dash_list} \n {date}')
                    count+=1
                    print(innershell)
        
        print('###########################')    
        return count, rows

        # count = 0
        # for outershell in user_data:
        #     for innershell in outershell:   
        #         if len(innershell) >= 7 and innershell[2] != '' and (innershell[6] == 'BD' or 'Product' or 'Treasury' or 'Creative & Design' or 'Dev/Engineering' or 'Growth' or 'Expenses' or 'MVI' or 'Analytics' or 'People Org & Community' or 'Institutional Business' or 'MetaGov' or 'Other' or 'Lang-Ops') :
        #             dash_list = list(map(is_empty, innershell))
        #             DB.AddContribution(db, date.strftime("%m/%y"), dash_list[0], dash_list[1], dash_list[2], dash_list[3], dash_list[4], dash_list[5], dash_list[6], dash_list[7])
        #             count +=1
        #             print(f'{dash_list} \n {date}')

        # return count, rows



class NewUser:
    def __init__(self):
            self.db = 'index_contribution.db'
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
        self.raw_input = sheet.get_worksheet_by_id(raw_input_creds) #connects with raw input sheet
        self.owl_ids = sheet.get_worksheet_by_id(owl_sheet_creds) #connects with owl id reference worksheet


    #collects all the users info stored in Owl ID reference worksheet and puts them into Contributor TABLE
    def collectAllOwlIDs(self): 
        db = 'index_contribution.db'
        range = ['A2:B165']
        userInfo = self.owl_ids.batch_get(range)

        for outershell in userInfo:
            for innershell in outershell:
                if innershell[0] != '':
                    DB.AddContributor(db, innershell[0], innershell[1])



    #change wallet address.    
    #They might want this to connect to google sheets database....    
    def changeWalletAddress(self, owlId, walletAddress): 
        db = 'index_contribution.db'
        DB.changeWallet(db, owlId, walletAddress)



    #should pass in date
    def updateMasterSheet(self): #updates the mastersheet.
        dbname = 'index_contribution.db'
        connection = sqlite3.connect(dbname)
        c = connection.cursor() 

        date = datetime.datetime.now().strftime("%m/%y")
        today_date = datetime.date.today()
        first = today_date.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        
        c.execute("SELECT USER_ID, DISCORD_NAME, CONTRIBUTION_INFO, LINKS, OTHER_NOTES, HOURS, FUNCTIONAL_GROUP, PRODUCT FROM SINGLECONTRIBUTION WHERE DATE = ? OR DATE = ?", (lastMonth.strftime("%m/%y"),date))
        
        l = list(c.fetchall())
        l2 = list(map(list, l)) #holds all the contribution data for the month

        row_id = 4

        #transforms the the owl id into integers to allow for to sort all the contributions.
        # This was made because some people forget to submit all data at once, this allows for the master sheet to have continuity between all contributors. 
        def sort_list(data):
            for x in range(len(data)):
                if data[x][0][0:4] == '#owl':
                    data[x][0] = 73
                elif data[x][0][0:5] == 'Chase':
                    data[x][0] = 121
                elif data[x][0][0:3] == '#00':
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
            data = [owl_id, f"=VLOOKUP(A{row_id},'Owl ID reference'!$A$2:$C$600,2,FALSE)", 'Contribution', 'Link to Work', 'Other notes', 'Time contributed (Hours)', '# Functional area', 'Product',
            f'=sumifs($I$3:$I$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Treasury")', f'=sumifs($J$3:$J$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Product")', f'=sumifs(K$3:K$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"BD")',
            f'=sumifs($L$3:$L$1032,$B$3:B$1032,B{row_id},$G$3:$G$1032,"Creative & Design")', f'=sumifs($M$3:$M$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Dev/Engineering")', f'=sumifs($N$3:$N$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Growth")',
            f'=sumifs(O$3:O$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Expenses")', f'=sumifs(P$3:P$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"MVI")', f'=sumifs(Q$3:Q$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Analytics")',
            f'=sumifs(R$3:R$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Institutional Business")', f'=sumifs(S$3:S$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"People, Org & Community")', f'=sumifs(T$3:T$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"MetaGov")',
            f'=sumifs(U$3:U$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Other")', f'=sumifs(V$3:V$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Lang-Ops")', f'=sum(I{row_id}:V{row_id})+X{row_id + 1}', '', '', f'=(W{row_id}/$B$1)+Y{row_id + 1}']


            self.raw_input.insert_row(data, index = row_id, value_input_option='USER_ENTERED')


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
            self.raw_input.format(f'C{row_id}:H{row_id}', {
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
            self.raw_input.format(f'I{row_id}:Z{row_id}', {
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
        # time.sleep(60)######################################################

        # creates the list of lists for row W and Z formulas 
        # this allows for a batch_update. 
        wsum = []
        zsum= []
        for x in range(len(newlist)):
            wsum.append(f'=SUM(I{row_id+x}:V{row_id+x})')
            zsum.append(f'=(W{row_id+x}/$B$1)')

        w_list = [[x] for x in wsum]
        z_list = [[x] for x in zsum]

        #batch update all forumlas to master sheet
        self.raw_input.batch_update([{
           'range': 'W4',
            'values': w_list, 
        }, {'range': 'Z4',
            'values': z_list,
            }], value_input_option = 'USER_ENTERED')

        #time.sleep(60)######################################################
        ##### creates the titles for each person #######
        first_owl = ['holder'] #used as a starting point
        title_number = 4  
        for x in range(len(newlist)):
            ids = newlist[x][0]
            if ids != first_owl:
                first_owl = ids
                insert_title(first_owl, title_number)
                time.sleep(3)
                title_number +=2
            else:
                title_number +=1
        
    


    #Clears last MasterSheet Data
    #Resets sheet format
    def clearLastMonthsData(self):
        range = ['A4:Z1500']
        self.raw_input.format("A4:Z1500", {
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


