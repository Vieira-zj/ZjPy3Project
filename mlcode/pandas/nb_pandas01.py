# %%
# Introducing Pandas Objects
import numpy as np
import pandas as pd
np.__version__

# %%
# The Pandas Series Object
data = pd.Series([0.25, 0.5, 0.75, 1.0])
print(data, '\n')

print(data.values, '\n')
print(data.index, '\n')
print(data[1], '\n')
print(data[1:3])

# %%
# Series as generalized NumPy array
data = pd.Series([0.25, 0.5, 0.75, 1.0], index=['a', 'b', 'c', 'd'])
print(data, '\n')
print(data['b'])

# %%
# Series as specialized dictionary
population_dict = {'California': 38332521, 'Texas': 26448193, 'New York': 19651127,
                   'Florida': 19552860, 'Illinois': 12882135}
population = pd.Series(population_dict)
print(population, '\n')
print(population.values, '\n')

print(population['California'], '\n')
print(population['California':'Illinois'])

# %%
# Constructing Series objects
pd.Series({2: 'a', 1: 'b', 3: 'c'}, index=[3, 2])



# %%
# The Pandas DataFrame Object
area_dict = {'California': 423967, 'Texas': 695662, 'New York': 141297,
             'Florida': 170312, 'Illinois': 149995}
area = pd.Series(area_dict)
states = pd.DataFrame({'population': population, 'area': area})
print(states, '\n')

print(states.index, '\n')
print(states.columns)

# %%
# DataFrame as specialized dictionary
data = states['area']
print(type(data))
data

# %%
# Constructing DataFrame objects
# From a single Series object
pd.DataFrame(population, columns=['population'])

# %%
# From a list of dicts
data = [{'a': i, 'b': i*2} for i in range(3)]
pd.DataFrame(data)

# %%
pd.DataFrame([{'a': 1, 'b': 2}, {'b': 3, 'c': 4}])

# %%
# From a two-dimensional NumPy array
pd.DataFrame(np.random.rand(3, 2), columns=[
             'foo', 'bar'], index=['a', 'b', 'c'])



# %%
# The Pandas Index Object
ind = pd.Index([2, 3, 5, 7, 11])
ind

# %%
# Index as immutable array
print(type(ind), '\n')
print(ind.size, ind.shape, ind.ndim, ind.dtype, '\n')

print(ind[1], '\n')
print(ind[::2])

# %%
# Index as ordered set
indA = pd.Index([1, 3, 5, 7, 9])
indB = pd.Index([2, 3, 5, 7, 11])
print(indA | indB, '\n')  # union
print(indA & indB, '\n')  # intersection
print(indA ^ indB)  # symmetric difference



# %%
# Data Indexing and Selection
# Data Selection in Series
data = pd.Series([0.25, 0.5, 0.75, 1.0], index=['a', 'b', 'c', 'd'])
data
print('a' in data, '\n')
print(data.keys(), '\n')
print(list(data.items()))

# %%
data['e'] = 1.25
data

# %%
# Series as one-dimensional array
print(data['a':'c'], '\n')
print(data[0:2], '\n')
print(data[['a', 'e']], '\n')

# %%
cond = (data > 0.3) & (data < 0.8)
print(data[cond])

# %%
# Indexers: loc, iloc, and ix
data = pd.Series(['a', 'b', 'c'], index=[1, 3, 5])
print(data, '\n')
print(data[1], '\n')
print(data[1:3])

# %%
# explicit index
print(data.loc[1], '\n')
print(data.loc[1:3], '\n')

# implicit Python-style index
print(data.iloc[1], '\n')
print(data.iloc[1:3])



# %%
# Data Selection in DataFrame
# DataFrame as a dictionary
area = pd.Series({'California': 423967, 'Texas': 695662,
                  'New York': 141297, 'Florida': 170312,
                  'Illinois': 149995})
pop = pd.Series({'California': 38332521, 'Texas': 26448193,
                 'New York': 19651127, 'Florida': 19552860,
                 'Illinois': 12882135})
data = pd.DataFrame({'area': area, 'pop': pop})
data

# %%
print(data['area'], '\n')
print(data.area, '\n')

data['density'] = data['pop'] / data['area']
data

# %%
# DataFrame as two-dimensional array
print(data.values, '\n')
print(data.values[0], '\n')
print(data.T)

# %%
print(data.loc[:'Illinois', :'pop'], '\n')
print(data.iloc[:3, :2], '\n')
data.ix[:3, :'pop']

# %%
cond = data['density'] > 100
data.loc[cond, ['pop', 'density']]

# %%
data.iloc[0, 2] = 90
data

# %%
# Additional indexing conventions
data['Florida':'Illinois']

# %%
data[1:3]

# %%
print('end')
