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
