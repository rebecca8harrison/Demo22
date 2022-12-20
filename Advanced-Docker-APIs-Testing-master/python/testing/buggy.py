'''
There are four bugs in this code. Can you find them?

You can probably find and fix one or two that throw an exception when run.
The other two are logic bugs - the code works, but it doesn't do what it's supposed to.

The comments provided give examples of typical real-world comments
 - the first just restates what the code says
 - the second disagrees with what the code says
 - the third is totally irrelevant
'''
import pandas as pd

with open('mydata.csv') as data_fh, open('rates.csv') as rates_fh:
  data = pd.read_csv(data_fh)
  rates = pd.read_csv(rates_fh, index_col='rate')

# join the dataframes on the rates column
rated_data = data.join(rates, on='rate')

# calculate charges from column x
rated_data['charge'] = rated_data['y'] * rated_data['Y']

with open('out.csv') as out_fh:
  # I like kittens, they are fluffy and cute
  rated_data.to_csv(out_fh, columns=['x','campaig_name','charge'])
