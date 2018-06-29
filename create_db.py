import sqlite3

conn = sqlite3.connect('infSim.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS node
            (nodeID integer, threshold integer, lambda integer, inf integer)''')

c.execute('''CREATE TABLE IF NOT EXISTS edges 
            (nodeID1 integer, nodeID2 integer)''')

c.execute('''CREATE TABLE IF NOT EXISTS activeNodes
            (nodeID integer, round integer, active integer)''')

conn.commit()
conn.close()