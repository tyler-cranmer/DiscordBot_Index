import sqlite3
from newContributor import Contributor


# function to create new database
# creates a Contribution table (user_id, discord name and wallet address)
# creates a singleContribution submission table(data, contribution info, links, other notes, functional group, user_id)
def create(dbname):
    connection = sqlite3.connect(dbname) #database name must end in .db
    c = connection.cursor() #cursor
    c.execute("""CREATE TABLE contributors (
        user_id INTEGER NOT NULL,
        discord_name TEXT NOT NULL,
        wallet_address TEXT NOT NULL
    )""")

    c.execute("""CREATE TABLE singleContribution (
        date TEXT NOT NULL,
        contribution_info TEXT,
        link_work BLOB,
        other_notes TEXT,
        functional_group TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES conributors(user_id)
    ) """)

    # c.execute("""CREATE TABLE monthlyContribution(
    #     date TEXT NOT NULL,
    #     user
    # )""")

    connection.commit() #commits changes to database
    connection.close()




# Function to add new contributors to the database under the contributor table.
# Username, Wallet address get inputed
# Contributor class generates user id number. 
# Stores username, wallet address and user id. 
def AddContributor(dbname, username, walletAddress):
    connection = sqlite3.connect(dbname) #database name must end in .db
    c = connection.cursor() #cursor


    if(username == "" or not isinstance(username, str)):
        raise ValueError("Invalid Discord Name")
    elif(walletAddress== "" or not isinstance(walletAddress, str) or not walletAddress[:2] == '0x'):
        raise ValueError('Invalid Wallet Address')
    else:
        new_contributor = Contributor(f'{username}', f'{walletAddress}')
        c.execute("INSERT INTO contributors VALUES (:id, :username, :wallet)", {'id': new_contributor.id, 'username': new_contributor.username, 'wallet': new_contributor.walletAddress})
    
    connection.commit()
    connection.close()


# Function to insert a single contribution into Table.
# params (database name, user id, date, contribution info, links, other notes, functional group)

def AddContribution(dbname, user_id, date, contribution_info, link_work, other_notes, functional_group):
    connection = sqlite3.connect(dbname) #database name must end in .db
    c = connection.cursor() #cursor

    c.execute("INSERT INTO singleContribution VALUES (:subDate, :con_info, :link, :notes, :fun_group, :id)", {'subDate': date, 'con_info': contribution_info, 'link': link_work, 'notes': other_notes, 'fun_group': functional_group, 'id': user_id})
    connection.commit()
    connection.close()

def main():
    db = 'index_contribution.db'
    connection = sqlite3.connect(db) #database name must end in .db
    c = connection.cursor() #cursor

    info = ['1', '8/22', 'Automated new joiner process with Zapier', 'https://www.notion.so/Task-Streamline-New-Joiner-onboarding-489ca1e353994f71972afdec8509915e', 'Zaps for 1) inviting new members, 2) adding roles to Discord 3) holding calls in DiscordNow handed over to bradwmorris (Also logged this in Bronze Owl Quest)', 'BD']

    create(db)
    AddContributor(db, 'Teewhy', '0x45678')
    AddContributor(db, '0xModene', '0x12345')
    AddContribution(db, info[0], info[1], info[2], info[3], info[4], info[5])

    c.execute("SELECT * FROM contributors WHERE discord_name=:username", {'username': 'Teewhy'} )
    print(c.fetchall())
    c.execute("SELECT * FROM contributors WHERE discord_name=:username", {'username': '0xModene'} )
    print(c.fetchall())
    c.execute("SELECT * FROM singleContribution WHERE user_id=:id", {'id': 1} )
    print(c.fetchall())



if __name__ == '__main__':
    main()