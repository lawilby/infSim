import sqlite3
import numpy as np
from itertools import combinations

directory_name = '/Users/laurawilby/dev/experiments_data/new'

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

conn = sqlite3.connect(directory_name + '/results.db')
conn.row_factory = sqlite3.Row

results_query = conn.execute('''SELECT inf, rounds FROM results''')

influence = list()
rounds = list()

for result in results_query:

    influence.append(result['inf'])
    rounds.append(result['rounds'])


influence_vector = np.array(influence)
rounds_vector = np.array(rounds)

# print(influence_vector)
# print(rounds_vector)

# calculate dot products to get SST, SSA, ... etc. 

Sum_of_Squares_Influence = list()
Sum_of_Squares_Rounds = list()

for column in columns:

    dot_product_influence = np.vdot(column, influence_vector)
    dot_product_rounds = np.vdot(column, rounds_vector)
    Sum_of_Squares_Influence.append(dot_product_influence)
    Sum_of_Squares_Rounds.append(dot_product_rounds)

# print(Sum_of_Squares_Influence)
# print(Sum_of_Squares_Rounds)

# calculate percentages as SSA/SST etc.

percentages_influence = list()
percentages_rounds = list()

for inf, rou in zip(Sum_of_Squares_Influence, Sum_of_Squares_Rounds):

    inf_percent = inf/Sum_of_Squares_Influence[0]
    round_percent = rou/Sum_of_Squares_Rounds[0]
    percentages_influence.append(inf_percent)
    percentages_rounds.append(round_percent)

labels = ['dataset', 'thresh', 'lambda', 'inc', 'decay', 'budget']
column_labels = list(['all'])
column_labels.extend(labels)

for (a,b) in combinations(labels,2):
    column_labels.append('{} {}'.format(a,b))

for (a,b,c) in combinations(labels,3):
    column_labels.append('{} {} {}'.format(a,b,c))

for (a,b,c,d) in combinations(labels,4):
    column_labels.append('{} {} {} {}'.format(a,b,c,d))

for (a,b,c,d,e) in combinations(labels,5):
    column_labels.append('{} {} {} {} {}'.format(a,b,c,d,e))

with open('{}/results.txt'.format(directory_name), 'w') as results_text:

    results_text.write('Percentage Influenced\n')
    results_text.write('Variables : Effect,  Percent Influenced\n')
    for label, percent, inf in zip(column_labels,percentages_influence,influence):

        results_text.write('{} : {},  {}\n'.format(label, round(percent*100,2), inf))

    results_text.write('Rounds\n')
    results_text.write('Variables : Effect,  Rounds\n')

    for label, percent, ro in zip(column_labels, percentages_rounds, rounds):

        results_text.write('{} : {},  {}\n'.format(label, round(percent*100,2), ro))