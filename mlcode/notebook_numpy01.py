# %%
import numpy as np
# Understanding Data Types

# %%
# integer array
np.array([1, 4, 2, 5, 3])

# %%
np.array([1, 2, 3, 4], dtype='float32')

# %%
# create a length-10 integer array filled with zeros
np.zeros(10, dtype=int)

# %%
# create a 3x5 floating-point array filled with ones
np.ones((3, 5), dtype=float)

# %%
# create a 3x5 array filled with 3.14
np.full((3, 3), 3.14)

# %%
# create an array of five values evenly spaced between 0 and 1
np.linspace(0, 1, 5)

# %%
# create a 3x3 array of uniformly distributed
# random values between 0 and 1
np.random.random((3, 3))


# %%
# create a 3x3 array of normally distributed random values
# with mean 0 and standard deviation 1
np.random.normal(0, 1, (3, 3))

# %%
# create a 3x3 array of random integers in the interval [0, 10)
np.random.randint(0, 10, (3, 3))

# %%
