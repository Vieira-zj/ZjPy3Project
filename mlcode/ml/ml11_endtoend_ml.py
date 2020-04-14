# %%
import pandas as pd

housing_path = 'data/housing.csv'
housing = pd.read_csv(housing_path)
housing.head()


# %%
# 补充
# hist() 柱状图
import numpy as np
import pandas as pd
range1 = pd.Series(np.arange(100))
range2 = pd.Series(np.random.randint(0, 100, size=100))
df = pd.DataFrame({'range1': range1, 'range2': range2})
df.head()

# %%
%matplotlib inline
import matplotlib.pyplot as plt
df.hist(bins=10, figsize=(20, 15))
plt.show()

# %%
# filter condition
scope = pd.Series(np.arange(10))
label = pd.Series(np.random.choice(['x', 'y'], size=10))
df = pd.DataFrame({'scope': scope, 'label': label})
df

# %%
cond = df['scope'] % 2 == 0
print(df.loc[cond])
print()
print(df.loc[~cond])

# %%
cond = df['label'] == 'y'
print(df.loc[cond])
print()
print(df.loc[~cond])


# %%
print('end to end ml demo done')
