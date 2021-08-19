import sqlite3

def create(dbname):
    connection = sqlite3.connect(dbname) #database name must end in .db
    c = connection.cursor() #cursor
    c.execute("""CREATE TABLE Contributors (
        id integer,
        discord_name text,
        contribution_info text,
        link_work text,
        other_notes text,
        functional_area text
    )""")

    connection.commit() #commits changes to database
    connection.close()


# def addContributor(dbname, username, )

def main():
    create('index_contributors.db')


if __name__ == '__main__':
    main()