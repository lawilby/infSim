import sqlite3
import numpy as np
from itertools import combinations

directory_name = '/local-scratch/lw-data/aug29/enron/inc_0_1_budget_1_15'
n_experiments = 32
factors = ['thresh', 'inc', 'lambda', 'budget', 'decay']

one = list()
i = 2

while (n_experiments/i > 1):

    '''Terminates when i is equal to the number of experiments'''

    half_pattern_size = int(n_experiments/i)
    pattern_repeats   = int(n_experiments/(half_pattern_size*2))

    pattern = [1]*half_pattern_size
    pattern.extend([-1]*half_pattern_size)

    one.append(np.tile(pattern,pattern_repeats))

    i=i*2


columns        = list(one)
factor_vectors = list()

j = 2

while j <= len(one):

    '''Terminates when j is bigger then the number of factors'''
    combinations_to_multiply = combinations(one,j)
    factor_combinations = combinations(factors,j)

    for column_combination in combinations_to_multiply:

        new_column = np.ones(n_experiments)
        for column in column_combination:

            new_column*column

        columns.append(new_column)

    factor_vector = list()

    for factor_combination in factor_combinations:

        print(factor_combination)
        for factor in factors:

            if factor in factor_combination:

                factor_vector.append(1)

            else:

                factor_vector.append(0)

    factor_vectors.append(factor_vector)


    j = j + 1


# connect to results db and build y-s as seperate np array

conn = sqlite3.connect(directory_name + '/results.db')
conn.row_factory = sqlite3.Row

results_query = conn.execute('''SELECT inf, rounds, benchmark FROM results''')

influence = list()
rounds = list()
benchmark = list()

for result in results_query:

    influence.append(result['inf'])
    rounds.append(result['rounds'])
    benchmark.append(result['benchmark'])


influence_vector = np.array(influence)
rounds_vector = np.array(rounds)
benchmark_vector = np.array(benchmark)


# calculate dot products to get SST, SSA, ... etc. 

Influence_qs = list()
Rounds_qs = list()
Benchmark_qs = list()

for column in columns:

    dot_product_influence = np.vdot(column, influence_vector)
    dot_product_rounds = np.vdot(column, rounds_vector)
    dot_product_benchmark = np.vdot(column, benchmark_vector)
    Influence_qs.append(dot_product_influence)
    Rounds_qs.append(dot_product_rounds)
    Benchmark_qs.append(dot_product_benchmark)


# calculate percentages as SSA/SST etc.

Influence_qs = np.array(Influence_qs)
Rounds_qs = np.array(Rounds_qs)
Benchmark_qs = np.array(Benchmark_qs)

Influence_qs = np.divide(Influence_qs, n_experiments)
Rounds_qs = np.divide(Rounds_qs, n_experiments)
Benchmark_qs = np.divide(Benchmark_qs, n_experiments)

Influence_qs = np.square(Influence_qs)
Rounds_qs = np.square(Rounds_qs)
Benchmark_qs = np.square(Benchmark_qs)

Influence_qs = np.multiply(n_experiments,Influence_qs)
Rounds_qs = np.multiply(n_experiments, Rounds_qs)
Benchmark_qs = np.multiply(n_experiments, Benchmark_qs)

SST_Inf = np.sum(Influence_qs)
SST_Rou = np.sum(Rounds_qs)
SST_Ben = np.sum(Benchmark_qs)

percentages_influence = list()
percentages_rounds = list()
percentages_benchmark = list()

for inf, rou, ben in zip(Influence_qs, Rounds_qs, Benchmark_qs):

    inf_percent = inf/SST_Inf
    round_percent = rou/SST_Rou
    bench_percent = ben/SST_Ben
    percentages_influence.append(inf_percent)
    percentages_rounds.append(round_percent)
    percentages_benchmark.append(bench_percent)


with open('{}/results.csv'.format(directory_name), 'w') as results_text:

    header = 'percent_inf,rounds,benchmark,{}\n'.format(factors)
    results_text.write(header)

    for percent, rounds, bench, vector in zip(percentages_influence,percentages_rounds,percentages_benchmark,factor_vectors):

        results_text.write('{},{},{},{}\n'.format(percent,rounds,bench,vector))



