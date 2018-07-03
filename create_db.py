import sqlite3
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

conn = sqlite3.connect(config['FILES']['DB'])

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS node
            (nodeID INTEGER PRIMARY KEY, 
             threshold INTEGER, 
             lambda INTEGER, 
             inf INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS edges 
            (nodeID1 INTEGER, 
             nodeID2 INTEGER)''')

'''
edges cannot have a unique index (PK) on either column. Might want a multipart PK in future?
'''
c.execute('''CREATE INDEX IF NOT EXISTS nodeID1 ON edges (nodeID1)''')

c.execute('''CREATE TABLE IF NOT EXISTS activeNodes
            (nodeID INTEGER PRIMARY KEY, 
             round INTEGER, 
             active INTEGER)''')

'''
In case of crash in the middle of a transaction, db will likely be inconsistent and need to be re-created due to use of this PRAGMA.
For our purposes, this seems like an OK trade-off to speed up execution.
'''
conn.execute('PRAGMA synchronous = OFF')  

conn.commit()
conn.close()