# %%
# Aggregation and Grouping
import numpy as np
import pandas as pd
print(np.__version__)

class display(object):
    '''Display HTML representation of multiple objects'''

    template = '''<div style="float: left; padding: 10px;">
    <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
    </div>'''

    def __init__(self, *args):
        self.args = args

    def _repr_html_(self):
        return '\n'.join(self.template.format(a, eval(a)._repr_html_())
                         for a in self.args)

    def __repr__(self):
        return '\n\n'.join(a + '\n' + repr(eval(a))
                           for a in self.args)

# %%
# Planets Data
import seaborn as sns
planets = sns.load_dataset('planets')
planets.shape

# %%
planets.head()

# %%
# Simple Aggregation in Pandas
rng = np.random.RandomState(42)
ser = pd.Series(rng.rand(5))
ser

# %%
ser.mean(), ser.sum()

# %%
df = pd.DataFrame({'A': rng.rand(5), 'B': rng.rand(5)})
df

# %%
df.mean()

# %%
df.mean(axis='columns')

# %%
planets.dropna().describe()



# %%
# GroupBy: Split, Apply, Combine
df = pd.DataFrame({'key': ['A', 'B', 'C', 'A', 'B', 'C'],
                   'data': range(6)}, columns=['key', 'data'])
df

# %%
df.groupby('key').sum()

# %%
# The GroupBy object
# Column indexing
planets.groupby('method')['orbital_period'].median()

# %%
# Iteration over groups
for (method, group) in planets.groupby('method'):
    print("{0:30s} shape={1}".format(method, group.shape))

# %%
# Dispatch methods
planets.groupby('method')['year'].describe()



# %%
# Aggregate, filter, transform, apply
rng = np.random.RandomState(0)
df = pd.DataFrame({'key': ['A', 'B', 'C', 'A', 'B', 'C'],
                   'data1': range(6),
                   'data2': rng.randint(0, 10, 6)},
                  columns=['key', 'data1', 'data2'])
df

# %%
# Aggregation
df.groupby('key').aggregate(['min', np.median, max])

# %%
df.groupby('key').aggregate({'data1': 'min', 'data2': 'max'})

# %%
# Filtering
def filter_func(x):
    return x['data2'].std() > 4

display('df', "df.groupby('key').std()",
        "df.groupby('key').filter(filter_func)")

# %%
# Transformation
df.groupby('key').transform(lambda x: x - x.mean())

# %%
# The apply() method
def norm_by_data2(x):
    # x is a DataFrame of group values
    x['data1'] /= x['data2'].sum()
    return x

display('df', "df.groupby('key').apply(norm_by_data2)")

# %%
# Specifying the split key
L = [0, 1, 0, 1, 2, 0]
display('df', 'df.groupby(L).sum()')

# %%
display('df', "df.groupby(df['key']).sum()")

# %%
# A dictionary or series mapping index to group
df2 = df.set_index('key')
mapping = {'A': 'vowel', 'B': 'consonant', 'C': 'consonant'}
display('df2', 'df2.groupby(mapping).sum()')

# %%
# Any Python function
display('df2', 'df2.groupby(str.lower).mean()')

# %%
# Grouping example
decade = 10 * (planets['year'] // 10)
decade = decade.astype(str) + 's'
decade.name = 'decade'
decade.head()

# %%
planets.groupby(['method', decade])['number'].sum().unstack().fillna(0)

# %%
print('end')
