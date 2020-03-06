# %%
import numpy as np
np.__version__

# %%
# indexing
rand = np.random.RandomState(42)
x = rand.randint(100, size=10)
print(x, '\n')
idx = [3, 7, 4]
x[idx]

# %%
idx = np.array([[3, 7], [4, 5]])
x[idx]

# %%
y = np.arange(12).reshape((3, 4))
print(y, '\n')
row = np.array([0, 1, 2])
col = np.array([2, 1, 3])
y[row, col]

# %%
y[2, [2, 0, 1]]

# %%
# modifying values with indexing
x = np.arange(10)
i = np.array([2, 1, 8, 4])
x[i] = 99
print(x, '\n')
x[i] -= 10
print(x)



# %%
# selecting random points
mean = [0, 0]
cov = [[1, 2], [2, 5]]
X = rand.multivariate_normal(mean, cov, 100)
print(X.shape, '\n')

%matplotlib inline
import matplotlib.pyplot as plt
import seaborn

seaborn.set()  # for plot styling
plt.scatter(X[:, 0], X[:, 1])

# %%
indices = np.random.choice(X.shape[0], 20, replace=False)
print(indices, '\n')
selection = X[indices]
print(selection.shape, '\n')

plt.scatter(X[:, 0], X[:, 1], alpha=0.3)
plt.scatter(selection[:, 0], selection[:, 1], facecolor='none', s=200)



# %%
# sorting arrays
x = np.array([2, 1, 4, 3, 5])
print(np.sort(x), '\n')

i = np.argsort(x)
x[i]

# %%
# sorting along rows or columns
rand = np.random.RandomState(42)
X = rand.randint(0, 10, (4, 6))
print(X, '\n')
print(np.sort(X, axis=0), '\n')
print(np.sort(X, axis=1), '\n')

# %%
X = rand.rand(10, 2)
print(X.shape, '\n')
plt.scatter(X[:, 0], X[:, 1], s=100)


# %%
# structured arrays
data = np.zeros(4, dtype={'names': ('name', 'age', 'weight'),
                          'formats': ('U10', 'i4', 'f8')})
name = ['Alice', 'Bob', 'Cathy', 'Doug']
age = [25, 45, 37, 19]
weight = [55.0, 85.5, 68.0, 61.5]
data['name'] = name
data['age'] = age
data['weight'] = weight

print(data, '\n')
print(data['name'], '\n')  # get all names
print(data[0], '\n')  # get first row of data
print(data[-1]['name'])  # get name of last row

# Get names where age is under 30
data[data['age'] < 30]['name']

# %%
print('end')