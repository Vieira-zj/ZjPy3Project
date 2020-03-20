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
x

# %%
x[i] -= 10
x



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
np.sort(x)

# %%
i = np.argsort(x)
x[i]

# %%
# sorting along rows or columns
rand = np.random.RandomState(42)
X = rand.randint(0, 10, (4, 6))
X

# %%
np.sort(X, axis=0)

# %%
np.sort(X, axis=1)

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

# %%
data

# %%
# get all names
data['name']

# %%
# get first row of data
data[0]

# %%
# get name of last row
print(data[-1]['name'])

# Get names where age is under 30
data[data['age'] < 30]['name']



# %%
# 补充
# meshgrid（生成坐标矩阵X,Y)
import numpy as np

# 网格点的横纵坐标列向量
x = np.array([0, 1, 2])
y = np.array([0, 1])
X, Y = np.meshgrid(x, y)
print(type(X))
X, Y

# %%
import matplotlib.pyplot as plt
plt.plot(X, Y, color='red', marker='.', linestyle='')
plt.grid(True)
plt.show()

# %%
# flatten,ravel（将多维数组降位一维）
# flatten() 返回一份copy, 对copy所做的修改不会影响原始矩阵
# ravel() 返回的是view, 会影响原始矩阵
x = np.array([[1, 2], [3, 4], [5, 6]])
x.ravel()

# %%
x.reshape(-1)

# %%
print('numpy end')
