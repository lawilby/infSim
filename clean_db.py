### Empty data from infSim.db ##

import sqlite3

conn = sqlite3.connect('infSim.db')

c = conn.cursor()

c.execute('DELETE FROM node')
c.execute('DELETE FROM edges')
c.execute('DELETE FROM activeNodes')

conn.commit()
conn.close()