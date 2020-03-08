# %%
import numpy as np
np.__version__

# %%
# summing values in an array
arr = np.arange(1, 6)
np.sum(arr)

# %%
big_array = np.random.rand(1000000)
%timeit sum(big_array)
%timeit np.sum(big_array)

# %%
# minimum and maximum
print(np.min(big_array))
print(np.max(big_array))

# %%
arr = np.random.random((3, 4))
print(arr, '\n')
print(np.min(arr, axis=0), '\n')
print(np.max(arr, axis=1))



# %%
# broadcasting
a = np.array([0, 1, 2])
b = np.array([5, 5, 5])
a + b

# %%
x = np.ones((3, 3))
a + x

# %%
# newaxis 添加新的维度
x = np.random.randint(1, 8, size=5)
print(x, '\n')
print(x[np.newaxis, :], '\n')
print(x[:, np.newaxis], '\n')

# %%
# x and y have 50 steps from 0 to 5
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 50)[:, np.newaxis]
z = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

%matplotlib inline
import matplotlib.pyplot as plt

plt.imshow(z, origin='lower', extent=[0, 5, 0, 5], cmap='viridis')
plt.colorbar()



# %%
# comparison operators
x = np.array([1, 2, 3, 4, 5])
cond = x < 3
print(cond, '\n')
print(np.count_nonzero(cond), '\n')
print(np.sum(cond))

# %%
(x * 2) == (x ** 2)

# %%
rnd = np.random.RandomState(0)
y = rnd.randint(10, size=(3, 4))
print(y, '\n')

cond = y < 6
print(np.sum(cond), '\n')
print(np.sum(cond, axis=1), '\n')
np.all(y < 8, axis=1)

# %%
print(y, '\n')
cond = y < 5
print(cond, '\n')
print(y[cond])

# %%
z = np.arange(10)
cond = (z > 4) & (z < 8)
print(cond, '\n')
z[cond]

# %%
print('end')
