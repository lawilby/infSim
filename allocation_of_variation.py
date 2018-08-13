import sqlite3
import numpy as np
from itertools import combinations

directory_name = '/local-scratch/lw-data/new_2'

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

columns = list(one)

for (a,b) in combinations(one,2):
    columns.append(a*b)

for (a,b,c) in combinations(one,3):
    columns.append(a*b*c)

for (a,b,c,d) in combinations(one,4):
    columns.append(a*b*c*d)

for (a,b,c,d,e) in combinations(one,5):
    columns.append(a*b*c*d*e)

for (a,b,c,d,e,f) in combinations(one,6):
    columns.append(a*b*c*d*e*f)

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

Influence_qs = list()
Rounds_qs = list()

for column in columns:

    dot_product_influence = np.vdot(column, influence_vector)
    dot_product_rounds = np.vdot(column, rounds_vector)
    Influence_qs.append(dot_product_influence)
    Rounds_qs.append(dot_product_rounds)

# print(Sum_of_Squares_Influence)
# print(Sum_of_Squares_Rounds)

# calculate percentages as SSA/SST etc.

Influence_qs = np.array(Influence_qs)
Rounds_qs = np.array(Rounds_qs)

print(Influence_qs)
print(Rounds_qs)

Influence_qs = np.divide(Influence_qs, 64)
Rounds_qs = np.divide(Rounds_qs, 64)

print(Influence_qs)
print(Rounds_qs)


Influence_qs = np.square(Influence_qs)
Rounds_qs = np.square(Rounds_qs)

print(Influence_qs)
print(Rounds_qs)

Influence_qs = np.multiply(4096,Influence_qs)
Rounds_qs = np.multiply(4096, Rounds_qs)

SST_Inf = np.sum(Influence_qs)
SST_Rou = np.sum(Rounds_qs)

print(SST_Inf)
print(SST_Rou)

percentages_influence = list()
percentages_rounds = list()

for inf, rou in zip(Influence_qs, Rounds_qs):

    inf_percent = inf/SST_Inf
    round_percent = rou/SST_Rou
    percentages_influence.append(inf_percent)
    percentages_rounds.append(round_percent)

labels = ['dataset', 'thresh', 'lambda', 'inc', 'decay', 'budget']
column_labels = list(labels)

for (a,b) in combinations(labels,2):
    column_labels.append('{} {}'.format(a,b))

for (a,b,c) in combinations(labels,3):
    column_labels.append('{} {} {}'.format(a,b,c))

for (a,b,c,d) in combinations(labels,4):
    column_labels.append('{} {} {} {}'.format(a,b,c,d))

for (a,b,c,d,e) in combinations(labels,5):
    column_labels.append('{} {} {} {} {}'.format(a,b,c,d,e))

for (a,b,c,d,e,f) in combinations(labels,6):
    column_labels.append('{} {} {} {} {}'.format(a,b,c,d,e,f))

with open('{}/results.txt'.format(directory_name), 'w') as results_text:

    results_text.write('Percentage Influenced\n')
    results_text.write('Variables : Effect\n')
    for label, percent, inf in zip(column_labels,percentages_influence,influence):

        results_text.write('{} : {}\n'.format(label, round(percent*100,2), inf))

    results_text.write('Rounds\n')
    results_text.write('Variables : Effect\n')

    for label, percent, ro in zip(column_labels, percentages_rounds, rounds):

        results_text.write('{} : {}\n'.format(label, round(percent*100,2), ro))
