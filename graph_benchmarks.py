import matplotlib.pyplot as plt
import sqlite3

directory_name = '/Users/laurawilby/dev/experiments_data/November/YouTube/Decay1/vary_budget_incentives'

conn = sqlite3.connect(directory_name + '/results.db')
conn.row_factory = sqlite3.Row

# fig, axes = plt.subplots(nrows=2, ncols=2)
# fig.suptitle('Point in Simulation Benchmark Percentage of Total Influenced is Reached Under Different Incentive Values')

benchmarks = [.1,.2,.3,.4,.5,.6,.7,.8,.9]
incentives = [0,1,2,3]
budgets = [0.05,0.1,0.15,0.20,0.25]
# colours = {0.05:}
percentages_done = list()

for benchmark in benchmarks:

    plt.xlabel('Incentive')
    plt.ylabel('Percentage of Sim Completed')
    plt.title('')
    plt.axis([-1, 4, 0, 1])

    budget = 0.05

    benchmark_results = conn.execute('''SELECT budget, benchmark_val 
                                FROM results JOIN benchmark on benchmark.results_id = results.rowid
                                WHERE benchmark.benchmark = ?
                                ORDER BY budget''', (benchmark,))    
    
    for result_row in benchmark_results: 

        print(budget)
        print(result_row['budget']) 
        
        if budget != result_row['budget']:

            if result_row['budget'] == 0.01:
                print('here')
                continue;
                    
            label = '{}'.format(budget)
            plt.plot(incentives, percentages_done, '.', label=label) 

            if result_row['budget'] not in budgets:

                break;

            budget = result_row['budget']
            percentages_done = list()        

        percentages_done.append(result_row['benchmark_val'])
        budgets.append(result_row['budget'])

    label = '{}'.format(budget)
    plt.plot(incentives, percentages_done, '.', label=label)  
    leg = plt.legend()
    percentages_done = list()

    plt.savefig('{}/benchmarks_{}.png'.format(directory_name,str(benchmark).replace('.','')))
    plt.cla()
    plt.clf()
