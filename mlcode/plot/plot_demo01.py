# %%
# Simple Line Plots
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# %%
# 画布
fig = plt.figure()
# 绘图区
ax = plt.axes()

# %%
fig = plt.figure()
ax = plt.axes()

import numpy as np
x = np.linspace(0, 10, 1000)
ax.plot(x, np.sin(x))

# %%
plt.plot(x, np.sin(x))

# %%
plt.plot(x, np.sin(x))
plt.plot(x, np.cos(x))

# %%
# Adjusting the Plot: Line Colors and Styles
# specify color by name
plt.plot(x, np.sin(x - 0), color='blue')
# short color code (rgbcmyk)
plt.plot(x, np.sin(x - 1), color='g')
# Grayscale between 0 and 1
plt.plot(x, np.sin(x - 2), color='0.75')
# Hex code (RRGGBB from 00 to FF)
plt.plot(x, np.sin(x - 3), color='#FFDD44')
# RGB tuple, values 0 to 1
plt.plot(x, np.sin(x - 4), color=(1.0, 0.2, 0.3))
# all HTML color names supported
plt.plot(x, np.sin(x - 5), color='chartreuse')

# %%
plt.plot(x, x + 0, linestyle='solid')
plt.plot(x, x + 1, linestyle='dashed')
plt.plot(x, x + 2, linestyle='dashdot')
plt.plot(x, x + 3, linestyle='dotted')

# %%
# For short, you can use the following codes
plt.plot(x, x + 4, linestyle='-')  # solid
plt.plot(x, x + 5, linestyle='--')  # dashed
plt.plot(x, x + 6, linestyle='-.')  # dashdot
plt.plot(x, x + 7, linestyle=':')  # dotted

# %%
# Adjusting the Plot: Axes Limits
plt.plot(x, np.sin(x))
plt.xlim(-1, 11)
plt.ylim(-1.5, 1.5)

# %%
plt.plot(x, np.sin(x))
plt.xlim(10, 0)
plt.ylim(1.2, -1.2)

# %%
plt.plot(x, np.sin(x))
plt.axis([-1, 11, -1.5, 1.5])

# %%
plt.plot(x, np.sin(x))
plt.axis('tight')

# %%
plt.plot(x, np.sin(x))
plt.axis('equal')

# %%
# Labeling Plots
plt.plot(x, np.sin(x))
plt.title('A Sine Curve')
plt.xlabel('x')
plt.ylabel('sin(x)')

# %%
plt.plot(x, np.sin(x), '-g', label='sin(x)')
plt.plot(x, np.cos(x), ':b', label='cos(x)')
plt.axis('equal')
plt.legend()

# %%
ax = plt.axes()
ax.plot(x, np.sin(x))
ax.set(xlim=(0, 10), ylim=(-2, 2),
       xlabel='x', ylabel='sin(x)',
       title='A Simple Plot')



# %%
# Simple Scatter Plots
x = np.linspace(0, 10, 30)
y = np.sin(x)
plt.plot(x, y, 'o', color='black')

# %%
rng = np.random.RandomState(0)
for marker in ['o', '.', ',', 'x', '+', 'v', '^', '<', '>', 's', 'd']:
    plt.plot(rng.rand(5), rng.rand(5), marker,
             label="marker='{0}'".format(marker))
plt.legend(numpoints=1)
plt.xlim(0, 1.8)

# %%
plt.plot(x, y, '-ok')

# %%
plt.plot(x, y, '-p', color='gray',
         markersize=15, linewidth=4,
         markerfacecolor='white',
         markeredgecolor='gray',
         markeredgewidth=2)
plt.ylim(-1.2, 1.2)

# %%
# Scatter Plots with plt.scatter
plt.scatter(x, y, marker='o')

# %%
rng = np.random.RandomState(0)
x = rng.randn(100)
y = rng.randn(100)
colors = rng.rand(100)
sizes = 1000 * rng.rand(100)

plt.scatter(x, y, c=colors, s=sizes, alpha=0.3, cmap='viridis')
plt.colorbar()  # show color scale

# %%
# plt.plot should be preferred over plt.scatter for large datasets.
# The reason is that plt.scatter has the capability to render a different size and/or color for each point,
# so the renderer must do the extra work of constructing each point individually.



# %%
# Visualizing Errors
# Basic Errorbars
x = np.linspace(0, 10, 50)
dy = 0.8
y = np.sin(x) + dy * np.random.randn(50)
plt.errorbar(x, y, yerr=dy, fmt='.k')

# %%
plt.errorbar(x, y, yerr=dy, fmt='o', color='black',
             ecolor='lightgray', elinewidth=3, capsize=0)



# %%
# Density and Contour Plots
def f(x, y):
    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

# %%
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)
Z.shape

# %%
plt.contour(X, Y, Z, colors='black')

# %%
plt.contour(X, Y, Z, 20, cmap='RdGy')

# %%
plt.contourf(X, Y, Z, 20, cmap='RdGy')
plt.colorbar()

# %%
print('end')
