import sqlite3
from newContributor import Contributor

################################################################################
#           CONTRIBUTION TABLE
#   USER_ID    DISCORD_NAME   WALLET_ADDRESS 
# ----------   ------------   --------------  
################################################################################
#        SINGLE CONTRIBUTION TABLE
# USER_ID    DATE     CONTRIBUTION_INFO   LINKS    OTHER_NOTES  FUNCTIONAL_GROUP 
#--------  --------   -----------------  -------   -----------  ----------------
################################################################################


##
# function to create new database
#
# PARAMS:
# dbname - name of database (str)
# creates a Contribution table (USER_ID, discord name and wallet address)
# creates a SINGLECONTRIBUTION submission table(data, contribution info, links, other notes, functional group, USER_ID)
##
def create(dbname):
    connection = sqlite3.connect(dbname) #database name must end in .db
    c = connection.cursor() #cursor
    c.execute("""CREATE TABLE CONTRIBUTORS (
        USER_ID INTEGER NOT NULL,
        DISCORD_NAME TEXT NOT NULL,
        WALLET_ADDRESS TEXT NOT NULL
    )""")

    c.execute("""CREATE TABLE SINGLECONTRIBUTION (
        USER_ID INTEGER NOT NULL,
        DATE TEXT NOT NULL,
        CONTRIBUTION_INFO TEXT,
        LINKS TEXT,
        OTHER_NOTES TEXT,
        FUNCTIONAL_GROUP TEXT NOT NULL,
        FOREIGN KEY(USER_ID) REFERENCES CONTRIBUTORS(USER_ID)
    ) """)

    # c.execute("""CREATE TABLE monthlyContribution(
    #     DATE TEXT NOT NULL,
    #     user
    # )""")

    connection.commit()
    connection.close()

##
# Function to add new contributors to the database under the contributor table.
# calls Contributor class, creates user_id and  stores values . 
#
# PARAMS
# dbname - database name (str)
# discordName - discord name (str)
# walletAddres - user metaMask wallet address(str)
# 
# INSERTS:
# discordName(str), wallet address(str) and user id(int) 
##
def AddContributor(dbname, discordName, walletAddress):
    connection = sqlite3.connect(dbname) #database name must end in .db
    c = connection.cursor() #cursor


    if(discordName == "" or not isinstance(discordName, str)):
        raise ValueError("Invalid Discord Name")
    elif(walletAddress== "" or not isinstance(walletAddress, str) or not walletAddress[:2] == '0x'):
        raise ValueError('Invalid Wallet Address')
    else:
        new_contributor = Contributor(f'{discordName}', f'{walletAddress}')
        c.execute("INSERT INTO CONTRIBUTORS VALUES (:user_id, :discord_name, :wallet)", {'user_id': new_contributor.id, 'discord_name': new_contributor.username, 'wallet': new_contributor.walletAddress})
    
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
def changeWallet(dbname, userId, walletAddress):
    connection = sqlite3.connect(dbname) #database name must end in .db
    c = connection.cursor() #cursor

    if(walletAddress=="" or not walletAddress[:2] == '0x'):
        raise ValueError('Invalid Wallet Address')
    else:
        c.execute("UPDATE CONTRIBUTORS SET WALLET_ADDRESS=:new_wallet WHERE USER_ID=:id", {'new_wallet': walletAddress, 'id': userId})
    connection.commit()
    connection.close()

##
# Function to insert a single contribution into Table.
#
# PARAMS:
# dbname - database name (str)
# USER_ID - index ID (int)
# CONTRIBUTION_INFO - contribution description (str)
# LINKS - contribution links (str)
# OTHER_NOTES - additional notes (str)
# FUNCTIONAL_GROUP - function group (str)
#
# INSERT:
#(dbname, USER_ID, DATE, CONTRIBUTION_INFO, LINKS, OTHER_NOTES, FUNCTIONAL_GROUP) into songle contribution table
##
def AddContribution(dbname, USER_ID, DATE, CONTRIBUTION_INFO, LINKS, OTHER_NOTES, FUNCTIONAL_GROUP):
    connection = sqlite3.connect(dbname)
    c = connection.cursor() 

    c.execute("INSERT INTO SINGLECONTRIBUTION VALUES (:id, :sub_date, :con_info, :link, :notes, :func_group)", {'id': USER_ID, 'sub_date': DATE, 'con_info': CONTRIBUTION_INFO, 'link': LINKS, 'notes': OTHER_NOTES, 'func_group': FUNCTIONAL_GROUP})
    connection.commit()
    connection.close()

def main():
    db = 'index_contribution.db'
    connection = sqlite3.connect(db) #database name must end in .db
    c = connection.cursor() #cursor

    info = [1, '8/22', 'Automated new joiner process with Zapier', 'https://www.notion.so/Task-Streamline-New-Joiner-onboarding-489ca1e353994f71972afdec8509915e', 'Zaps for 1) inviting new members, 2) adding roles to Discord 3) holding calls in DiscordNow handed over to bradwmorris (Also logged this in Bronze Owl Quest)', 'BD']

    create(db)
    AddContributor(db, 'Teewhy', '0x45678')
    c.execute("SELECT * FROM CONTRIBUTORS WHERE DISCORD_NAME=:discordName", {'discordName': 'Teewhy'} )
    print(c.fetchall())

    changeWallet(db, 1, '0x098732')
    c.execute("SELECT * FROM CONTRIBUTORS WHERE DISCORD_NAME=:discordName", {'discordName': 'Teewhy'} )
    print(c.fetchall())
   
    AddContributor(db, '0xModene', '0x12345')
    AddContribution(db, info[0], info[1], info[2], info[3], info[4], info[5])

    c.execute("SELECT * FROM CONTRIBUTORS WHERE DISCORD_NAME=:discordName", {'discordName': '0xModene'} )
    print(c.fetchall())
    c.execute("SELECT * FROM SINGLECONTRIBUTION WHERE USER_ID=:id", {'id': 1} )
    print(c.fetchall())
    


if __name__ == '__main__':
    main()