### Empty data from infSim2.db ##

import sqlite3
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

conn = sqlite3.connect(config['FILES']['DB'])

c = conn.cursor()

c.execute('DELETE FROM node')
c.execute('DELETE FROM edges')
c.execute('DELETE FROM activeNodes')

conn.commit()
conn.close()