import sqlite3

class Contributor:
    idCounter = 0
    def __init__(self, username, walletAddress):
        self.username = username
        self.walletAddress = walletAddress
        Contributor.idCounter +=1
        self.id = Contributor.idCounter

