import matplotlib.pyplot as plt
import sqlite3

directory_name = '/Users/laurawilby/dev/experiments_data/November/amazon/Decay1/vary_budget_incentives'

conn = sqlite3.connect(directory_name + '/results.db')
conn.row_factory = sqlite3.Row


total_percentage_influenced_results = conn.execute('SELECT inc, budget, inf FROM results')


plt.xlabel('Budget')
plt.ylabel('Percentage Influenced')
plt.title('Percentage Influenced Varying Budget and Incentive')
plt.axis([0, .7, 45, 80])

incentive = 0.
percentages_influenced = list()
budgets = list()

for result_row in total_percentage_influenced_results:

    if incentive != result_row['inc']:

        label = '{}'.format(incentive)
        plt.plot(budgets, percentages_influenced, '4', label=label)  
        incentive = result_row['inc']
        percentages_influenced = list()
        budgets = list()


    percentages_influenced.append(result_row['inf'])
    budgets.append(result_row['budget'])

label = '{}'.format(incentive)
plt.plot(budgets, percentages_influenced, '4', label=label)  
incentive = result_row['inc']
percentages_influenced = list()
budgets = list()

leg = plt.legend()
plt.savefig('{}/inf_by_budget_inc.png'.format(directory_name))
       
