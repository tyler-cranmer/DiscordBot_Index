import sqlite3


#####################################################################################################
#           CONTRIBUTORS TABLE
#   USER_ID    DISCORD_NAME   WALLET_ADDRESS 
# ----------   ------------   --------------  
#####################################################################################################
#        SINGLE CONTRIBUTION TABLE
# DATE   USER_ID   DISCORD_NAME  CONTRIBUTION_INFO   LINKS  OTHER_NOTES  FUNCTIONAL_GROUP   PRODUCT
# -----  -------   ------------  -----------------   -----  -----------  ----------------   -------
#####################################################################################################


##
# function to create new database
#
# PARAMS:
# dbname - name of database (str)
# creates a Contribution table (OWL_ID, discord name)
# creates a SINGLECONTRIBUTION submission table(Date, OWL_ID, Discord Name, Contribution Info, Has Discussed?, Links, Other_Notes, Hours, Nest, Pod, Lead to Review)
##
class DB:
    def create(dbname):
        connection = sqlite3.connect(dbname) #database name must end in .db
        c = connection.cursor() #cursor
        c.execute("""CREATE TABLE CONTRIBUTORS (
            OWL_ID TEXT NOT NULL,
            DISCORD_NAME TEXT NOT NULL
        );""")
                    

        c.execute("""CREATE TABLE SINGLECONTRIBUTION (
            DATE TEXT NOT NULL,
            OWL_ID TEXT NOT NULL,
            DISCORD_NAME TEXT NOT NULL,
            CONTRIBUTION_INFO TEXT,
            HAS_DISCUSSED TEXT,
            LINKS TEXT,
            OTHER_NOTES TEXT,
            HOURS TEXT,
            NEST TEXT NOT NULL,
            POD TEXT,
            LEAD_TO_REVIEW TEXT,
            FOREIGN KEY(USER_ID) REFERENCES CONTRIBUTORS(USER_ID)
        );""")

        connection.commit()
        connection.close()

    ##
    # Function to add new contributors to the database under the contributor table.
    # calls Contributor class, creates user_id and  stores values . 
    #
    # PARAMS
    # dbname - database name (str)
    # owlId - owlId (str)
    # discordName - discord name (str)
    # walletAddres - user metaMask wallet address(str)
    # 
    # INSERTS:
    # owlID (str) discordName(str), wallet address(str) and user id(int) 
    ##
    def AddContributor(dbname, owlId, discordName, walletAddress):
        connection = sqlite3.connect(dbname) #database name must end in .db
        c = connection.cursor() #cursor


        if(discordName == "" or not isinstance(discordName, str)):
            raise ValueError("Invalid Discord Name")
        # elif(walletAddress== "" or not isinstance(walletAddress, str) or not walletAddress[:2] == '0x'):
        #     raise ValueError('Invalid Wallet Address')
        else:
            new_contributor = Contributor(f'{owlId}', f'{discordName}', f'{walletAddress}')
            c.execute("INSERT INTO CONTRIBUTORS VALUES (:owlId, :discord_name, :wallet);", {'owlId': new_contributor.owlId, 'discord_name': new_contributor.discordName, 'wallet': new_contributor.walletAddress})
        
        connection.commit()
        connection.close()

    ##
    #Change user wallet address
    #takes in userId and the new wallet address to be replaced. 
    #
    # PARAMS:
    # dbname - database name(str)
    # userId - index user ID number(int)
    # walletAddress - new wallet address to replace the old address(str)
    ##
    def changeWallet(dbname, owlId, walletAddress):
        connection = sqlite3.connect(dbname) #database name must end in .db
        c = connection.cursor() #cursor

        if(walletAddress=="" or not walletAddress[:2] == '0x'):
            raise ValueError('Invalid Wallet Address')
        else:
            c.execute("UPDATE CONTRIBUTORS SET WALLET_ADDRESS=:new_wallet WHERE USER_ID=:id;", {'new_wallet': walletAddress, 'id': owlId})
        connection.commit()
        connection.close()



    ##
    # Function to insert a single contribution into table.
    #
    # PARAMS:
    # dbname - database name (str)
    # date - from datetime (str) (mm/yy)
    # owlId - index ID (int)
    # discordName - discordName (str)
    # contributionInfo- contribution description (str)
    # has_discussed - was this job discussed with lead? (str)
    # links - contribution links
    # otherNotes - additional notes (str)
    # hours - hours worked (str)
    # nest - function group (str)
    # pod - product group (str)
    #
    # INSERT:
    #(dbname, DATE, owlId, discordName, contributionInfo, hasDiscussed, links, othernotes, hours, nest, pod) into songle contribution table
    ##


    def AddContribution(dbname, date, owlId, discordName, contributionInfo, hasDiscussed, links, otherNotes, hours, nest, pod):
        connection = sqlite3.connect(dbname)
        c = connection.cursor() 

        c.execute("INSERT INTO SINGLECONTRIBUTION VALUES (:date, :id, :discord, :con_info, :discuss, :link, :notes, :time, :func_group, :product_area);", 
            {'date': date, 
            'id': owlId, 
            'discord': discordName, 
            'con_info': contributionInfo, 
            'discuss': hasDiscussion,
            'link': links, 
            'notes': otherNotes, 
            'time': hours, 
            'func_group': nest,
            'product_area': pod
            })

        connection.commit()
        connection.close()


#creates a contributor class
class Contributor:
    def __init__(self, owlId, discordName, walletAddress):
        self.discordName = discordName
        self.walletAddress = walletAddress
        self.owlId = owlId

