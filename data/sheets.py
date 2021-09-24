import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
from data.database import DB
import datetime
import json

#https://collab-land.gitbook.io/collab-land/bots/discord
#https://wickbot.com/

with open("./config.json") as f:
    configData = json.load(f)

template_creds = configData["contributor_template"] #file_id for the new-contributor rewards sheet

class UserSheet:
    def __init__(self, discordName):
        self.discordName = discordName
        self.db = 'index_contribution.db'
        self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
            ]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name("gSheetCreds.json", self.scope) #access the json key you downloaded earlier 
        self.client = gspread.authorize(self.credentials) # authenticate the JSON key with gspread


    def collectContributorSheet(self): #collects info from sheets and puts it in SingleContributor TABLE
        sheet = self.client.open(str(self.discordName))
        contributionSheet = sheet.get_worksheet(0)
        ranges = ['A3:H51']
        user_data = contributionSheet.batch_get(ranges)
        db = self.db

        date = datetime.datetime.now()

        count = 0
        for outershell in user_data:
            for innershell in outershell:
                if len(innershell) >= 7 and (innershell[6] == 'BD' or 'Product' or 'Treasury' or 'Creative & Design' or 'Dev/Engineering' or 'Growth' or 'Expenses' or 'MVI' or 'Analytics' or 'People Org & Community' or 'Institutional Business' or 'MetaGov' or 'Other' or 'Lang-Ops'):
                    DB.AddContribution(db, date.strftime("%m/%y"), innershell[0], innershell[1], innershell[2], innershell[3], innershell[4], innershell[5], innershell[6], innershell[7])
                    count += 1
        return count


class NewUser:
    def __init__(self, discordName, email):
            self.discordName = discordName
            self.email = email
            self.template_id = template_creds
            self.folder_id = '11NsbfpsPsHOdXAveio7HbZrFuoboKS4D'
            self.db = 'index_contribution.db'
            self.scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
            ]
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name("gSheetCreds.json", self.scope) #access the json key you downloaded earlier 
            self.client = gspread.authorize(self.credentials) # authenticate the JSON key with gspread


    def create_spread_sheet(self):        
        self.client.copy(self.template_id, title=self.discordName, copy_permissions=False, folder_id= self.folder_id)
        new_sheet = self.client.open(str(self.discordName))
        new_sheet.share(str(self.email), perm_type='user', role='writer', notify = 'True', email_message='Did you get this?')    

        return new_sheet.url

class MasterControls:
    def __init__(self):
        scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name("gSheetCreds.json", scope) #access the json key you downloaded earlier 
        client = gspread.authorize(credentials) # authenticate the JSON key with gspread

        sheet = client.open("discordTests")  #opens discordTests google sheets
        self.owl_ids = sheet.worksheet("Sheet2")
        self.masterSheet = sheet.worksheet("MasterSheet main") #access Sheet1
        self.buisnessDevSheet = sheet.get_worksheet_by_id(463334884) 

        contributor_sheet = client.open_by_key(template_creds)
        self.owl_ids = contributor_sheet.get_worksheet(1)

    
    def collectAllOwlIDs(self): #collects all the users stored in Sheet2 of Owls and puts them into Contributor TABLE
        db = 'index_contribution.db'
        range = ['A2:C136']
        userInfoD = self.owl_ids.batch_get(range)

        for outershell in userInfoD:
            for innershell in outershell:
                DB.AddContributor(db, innershell[0], innershell[1], innershell[2])

        
        
    def changeWalletAddress(self, owlId, walletAddress):
        db = 'index_contribution.db'
        DB.changeWallet(db, owlId, walletAddress)

    #helper function to create name Titles for each candidate
    #controls the font colors
    def name(self, row_id, owl_id):
        self.buisnessDevSheet.batch_update([{
            'range': f'A{row_id}',
            'values': [[owl_id]],
        },{
            'range': f'B{row_id}',
            'values':  [[f"=VLOOKUP(A{row_id},'Owl ID reference'!$A$2:$C$600,2,FALSE)"]],
        },{
            'range': f'C{row_id}:H{row_id}',
            'values': [['Contribution', 'Link to work', 'Other notes', 'Time contributed (Hours)', '#Functional area', 'Product']],
        },{
            'range': f'I{row_id}',
            'values': [[f'=sumifs($I$3:$I$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Treasury")']]
        },{
            'range': f'J{row_id}',
            'values': [[f'=sumifs($J$3:$J$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Product")']]
        },{
            'range': f'K{row_id}',
            'values': [[f'=sumifs(K$3:K$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"BD")']]
        },{
            'range': f'L{row_id}',
            'values': [[f'=sumifs($L$3:$L$1032,$B$3:B$1032,B{row_id},$G$3:$G$1032,"Creative & Design")']]
        },{
            'range': f'M{row_id}',
            'values': [[f'=sumifs($M$3:$M$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Dev/Engineering")']]
        },{
            'range': f'N{row_id}',
            'values': [[f'=sumifs($N$3:$N$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Growth")']]
        },{
            'range': f'O{row_id}',
            'values': [[f'=sumifs(O$3:O$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Expenses")']]
        },{
            'range': f'P{row_id}',
            'values': [[f'=sumifs(P$3:P$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"MVI")']]
        },{
            'range': f'Q{row_id}',
            'values': [[f'=sumifs(Q$3:Q$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Analytics")']]
        },{
            'range': f'R{row_id}',
            'values': [[f'=sumifs(R$3:R$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Institutional Business")']]
        },{
            'range': f'S{row_id}',
            'values': [[f'=sumifs(S$3:S$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"People, Org & Community")']]
        },{
            'range': f'T{row_id}',
            'values': [[f'=sumifs(T$3:T$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"MetaGov")']]
        },{
            'range': f'U{row_id}',
            'values': [[f'=sumifs(U$3:U$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Other")']]
        },{
            'range': f'V{row_id}',
            'values': [[f'=sumifs(V$3:V$1032,$B$3:$B$1032,B{row_id},$G$3:$G$1032,"Lang-Ops")']]
        },{
            'range': f'W{row_id}',
            'values': [[f'=sum(I{row_id}:V{row_id})+X{row_id + 1}']]
        },{
            'range': f'Z{row_id}',
            'values': [[f'=(W{row_id}/$B$1)+Y{row_id + 1}']]
        }], value_input_option = 'USER_ENTERED')


        #Format the first A-B Cells
        self.buisnessDevSheet.format(f'A{row_id}:B{row_id}', {
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
        self.buisnessDevSheet.format(f'C{row_id}:H{row_id}', {
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
        self.buisnessDevSheet.format(f'I{row_id}:Z{row_id}', {
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



    #should pass in date
    def updateMasterSheet(self): #updates the mastersheet.
        dbname = 'index_contribution.db'
        connection = sqlite3.connect(dbname)
        c = connection.cursor() 

        date = datetime.datetime.now().strftime("%m/%y")
        
        c.execute("SELECT USER_ID, DISCORD_NAME, CONTRIBUTION_INFO, LINKS, OTHER_NOTES, HOURS, FUNCTIONAL_GROUP, PRODUCT FROM SINGLECONTRIBUTION WHERE DATE = ?", (date,))
        
        l = list(c.fetchall())
        newlist = list(map(list, l))

        pl = [['OWLID', 'DISCORD HANDLE', 'CONTRIBUTION', 'LINK TO WORK', 'OTHER NOTES', 'TIME CONTRIBUTED', '#FUNCTION AREA', 'PRODUCT']]

        first_name = pl[0][0] #used to get the owlid from pl
        
        row_id = 4
        index = 0

    #loop here to keep track of start value.
        for id in newlist:
            if id[0] != first_name:
                first_name = id[0]
                # self.buisnessDevSheet.update(f'A{row_id}:H{row_id}', pl) #used as a place holder for the BLUE Section
                self.name(row_id, first_name)
                row_id += 1
                self.buisnessDevSheet.update(f'A{row_id}:H{row_id}', [newlist[index]]) #updates contribution info from Col A - H
                self.buisnessDevSheet.update(f'W{row_id}', f'=SUM(I{row_id}:V{row_id})', raw=False) #updates col W cell functions
                self.buisnessDevSheet.update(f'Z{row_id}', f'=(W{row_id}/$B$1)', raw=False) #updates col Z cell functions
                row_id += 1
                index += 1
            elif id[0] == first_name:
                self.buisnessDevSheet.update(f'A{row_id}:H{row_id}', [newlist[index]]) #updates contribution info from Col A - H
                self.buisnessDevSheet.update(f'W{row_id}', f'=SUM(I{row_id}:V{row_id})', raw=False) #updates col W cell functions
                self.buisnessDevSheet.update(f'Z{row_id}', f'=(W{row_id}/$B$1)', raw=False) #updates col Z cell functions
                row_id +=1
                index +=1
            else:
                self.buisnessDevSheet.update(f'A{row_id}:H{row_id}', [newlist[index]]) #updates contribution info from Col A - H
                self.buisnessDevSheet.update(f'W{row_id}', f'=SUM(I{row_id}:V{row_id})', raw=False) #updates col W cell functions
                self.buisnessDevSheet.update(f'Z{row_id}', f'=(W{row_id}/$B$1)', raw=False) #updates col Z cell functions
                row_id +=1
                index +=1



    #Clears last MasterSheet Data
    def clearLastMonthsData(self):
        range = ['A4:Z50']
        self.buisnessDevSheet.batch_clear(range)
        self.buisnessDevSheet.format("A4:Z50", {
            "backgroundColor": {
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
        }})

