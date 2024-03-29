import sqlite3

def create_db(conn):

    conn.execute('''CREATE TABLE IF NOT EXISTS nodes
                (nodeID INTEGER PRIMARY KEY,
                threshold INTEGER,
                lambda INTEGER,
                inf INTEGER)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS edges
                (nodeID1 INTEGER,
                nodeID2 INTEGER)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS activeNodes
                (nodeID INTEGER,
                round INTEGER,
                power FLOAT)''')

    conn.execute('''CREATE INDEX IF NOT EXISTS nodeID ON activeNodes (nodeID)''')

    '''
    In case of crash in the middle of a transaction, db will likely be inconsistent and need to be re-created due to use of this PRAGMA.
    For our purposes, this seems like an OK trade-off to speed up execution.
    '''
    conn.execute('PRAGMA synchronous = OFF')

    conn.commit()

def create_results_db(conn):

    conn.execute('''CREATE TABLE IF NOT EXISTS results
                (date TEXT,
                 dataset TEXT,
                 thresh REAL,
                 lambda INTEGER,
                 inc REAL,
                 decay INTEGER,
                 budget INTEGER,
                 seed INTEGER,
                 rounds INTEGER,
                 inf REAL)''')

def add_benchmark_columns(conn):
   
    conn.execute('''CREATE TABLE IF NOT EXISTS benchmark (
                        results_id INTEGER,
                        benchmark REAL, 
                        benchmark_val REAL)''')

    conn.commit()