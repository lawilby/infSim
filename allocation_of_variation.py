import sqlite3
import numpy as np
from itertools import combinations

one = list()
'''threshold'''
one.append(np.repeat([1,-1],32))

'''lambda_val'''
pattern = [1]*16
pattern.extend([-1]*16)
one.append(np.tile(pattern,2))

'''selection size'''
pattern = [1]*8
pattern.extend([-1]*8)
one.append(np.tile(pattern,4))

'''composition'''
pattern = [1]*4
pattern.extend([-1]*4)
one.append(np.tile(pattern,8))

'''incentive'''
pattern = [1,1,-1,-1]
one.append(np.tile(pattern,16))

'''decay'''
pattern = [1,-1]
one.append(np.tile(pattern,32))

columns = list([np.ones(64)]) #Identity
columns.extend(one)

for (a,b) in combinations(one,2):
    columns.append(a*b)

for (a,b,c) in combinations(one,3):
    columns.append(a*b*c)

for (a,b,c,d) in combinations(one,4):
    columns.append(a*b*c*d)

for (a,b,c,d,e) in combinations(one,5):
    columns.append(a*b*c*d*e)

# connect to results db and build y-s as seperate np array
# calculate dot products to get SST, SSA, ... etc. 
# calculate percentages as SSA/SST etc.






