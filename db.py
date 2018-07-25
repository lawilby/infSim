import sqlite3

def create_db(conn):

    conn.execute('''CREATE TABLE IF NOT EXISTS nodes
                (nodeID INTEGER PRIMARY KEY,
                threshold INTEGER,
                inf INTEGER)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS edges
                (nodeID1 INTEGER,
                nodeID2 INTEGER)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS activeNodes
                (nodeID INTEGER,
                round INTEGER)''')

    conn.execute('''CREATE INDEX IF NOT EXISTS nodeID ON activeNodes (nodeID)''')

    '''
    In case of crash in the middle of a transaction, db will likely be inconsistent and need to be re-created due to use of this PRAGMA.
    For our purposes, this seems like an OK trade-off to speed up execution.
    '''
    conn.execute('PRAGMA synchronous = OFF')

    conn.commit()