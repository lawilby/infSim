import sqlite3
import numpy as np
from itertools import combinations

directory_name = '/Users/laurawilby/dev/experiments_data/November/YouTube/difficulty'
n_experiments = 16
factors = ['thresh', 'inc', 'lambda', 'budget']

one = list()
i = 2

while (n_experiments/i >= 1):

    '''Terminates when i is equal to the number of experiments'''

    half_pattern_size = int(n_experiments/i)
    pattern_repeats   = int(n_experiments/(half_pattern_size*2))

    pattern = [1]*half_pattern_size
    pattern.extend([-1]*half_pattern_size)

    one.append(np.tile(pattern,pattern_repeats))

    i=i*2

columns        = list(one)
factor_vectors = list([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

j = 2

while j <= len(one):

    '''Terminates when j is bigger then the number of factors'''
    combinations_to_multiply = combinations(one,j)
    factor_combinations = combinations(factors,j)

    for column_combination in combinations_to_multiply:

        new_column = np.ones(n_experiments)
        for column in column_combination:

            new_column = new_column*column

        columns.append(new_column)


    for factor_combination in factor_combinations:

        factor_vector = list()
        for factor in factors:

            if factor in factor_combination:

                factor_vector.append(1)

            else:

                factor_vector.append(0)

        factor_vectors.append(factor_vector)

    j = j + 1


conn = sqlite3.connect(directory_name + '/results.db')
conn.row_factory = sqlite3.Row

results_columns = ['Percentage Inf','Rounds']

results_query = conn.execute('''SELECT rowid, inf, rounds FROM results''')


results_lists = list()

for result in results_query:

    benchmarks = conn.execute('''SELECT benchmark, benchmark_val FROM benchmark WHERE results_id=?''', (result['rowid'],))

    row = list()

    row.append(result['inf'])
    row.append(result['rounds'])
        
    for benchmark in benchmarks:

        row.append(benchmark['benchmark_val'])
        col_name = '{} Benchmark'.format(benchmark['benchmark'])

        if not col_name in results_columns:

            results_columns.append(col_name)
    
    results_lists.append(row)

results_matrix = np.array(results_lists)


qs = [list() for column in results_columns]

for column in columns:

    dot_products = [np.vdot(column, vector) for vector in results_matrix.T]
    
    for i in range(len(dot_products)):

        qs[i].append(dot_products[i])


qs = [np.array(q) for q in qs]
qs = [np.divide(q, n_experiments) for q in qs]
qs = [np.square(q) for q in qs]
qs = [np.multiply(n_experiments, q) for q in qs]

totals = [np.sum(q) for q in qs]

percentages = [list() for column in results_columns]

for q, count in zip(qs, range(len(qs))):

    for num in q:

        if totals[count] > 0:
            percent = num/totals[count]
        
        else: 
            percent = 0

        percentages[count].append(percent)


with open('{}/results.csv'.format(directory_name), 'w') as results_text:

    t = results_columns

    h = ['{}'.format(i) for i in factors]

    t.extend(h)    

    header = ','.join(t)
    
    results_text.write(header)
    results_text.write('\n')


    for row_index in range(len(percentages[0])):

        r = list()
        for column_index in range(len(percentages)):

            r.append('{}'.format(round(percentages[column_index][row_index]*100,2)))
        
        v = ['{}'.format(i) for i in factor_vectors[row_index]]

        r.extend(v)

        line = ','.join(r)

        results_text.write(line)
        results_text.write('\n')



