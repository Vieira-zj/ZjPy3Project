# %%
import numpy as np
np.__version__
np.random.seed(0)

# %%
# integer array
np.array([1, 4, 2, 5, 3])

# %%
np.array([1, 2, 3, 4], dtype='float32')

# %%
# create a length-10 integer array filled with zeros
np.zeros(10, dtype=int)

# %%
# create a 3*5 floating-point array filled with ones
np.ones((3, 5), dtype=float)

# %%
# create a 3*5 array filled with 3.14
np.full((3, 5), 3.14)

# %%
# create an array of five values evenly spaced between 0 and 1
np.linspace(0, 1, 5)

# %%
# create a 3*3 array of uniformly distributed
# random values between 0 and 1
np.random.random((3, 3))

# %%
# create a 3*3 array of normally distributed random values
# with mean 0 and standard deviation 1
np.random.normal(0, 1, (3, 3))

# %%
# create a 3*3 array of random integers in the interval [0, 10)
np.random.randint(0, 10, (3, 3))



# %%
# numpy array attributes
arr = np.random.randint(10, size=(3, 4))  # two-dimensional array
print(type(arr), '\n')
print(arr, '\n')

print('ndim:', arr.ndim)
print('shape:', arr.shape)
print('size:', arr.size)
print('dtype:', arr.dtype)
print('nbytes:', arr.nbytes, 'bytes')

# %%
# array slicing: accessing subarrays
arr[:2, :3]  # two rows, three columns

# %%
arr[:, 0]  # first column of array

# %%
arr[0, :]  # first row of array

# %%
arr[0]  # equivalent to arr[0, :]

# %%
# concatenation of arrays
x = np.array([1, 2, 3])
y = np.array([3, 2, 1])
np.concatenate([x, y])

# %%
# concatenate along the first axis
grid = np.arange(6).reshape(2, 3)
np.concatenate([grid, grid])

# %%
# concatenate along the second axis (zero-indexed)
np.concatenate([grid, grid], axis=1)

# %%
# splitting of arrays
grid = np.arange(16).reshape((4, 4))
upper, lower = np.vsplit(grid, [2])
print(upper)
print(lower)

# %%
left, right = np.hsplit(grid, [2])
print(left)
print(right)



# %%
# array arithmetic
x = np.arange(4)
print(x)
print(np.add(x, 2))

# %%
# absolute value
x = np.array([-2, -1, 0, 1, 2])
np.abs(x)

# %%
# aggregates
x = np.arange(1, 6)
print(np.add.reduce(x))
print(np.add.accumulate(x))


# %%
print('end')
