### Empty data from infSim.db ##

import sqlite3

conn = sqlite3.connect('infSim.db')

c = conn.cursor()

c.execute('''DELETE FROM node''')


conn.close()