import sqlite3

class Contributor:
    def __init__(self, owlId, username, walletAddress):
        self.username = username
        self.walletAddress = walletAddress
        self.owlId = owlId

