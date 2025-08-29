import numpy as np
import matplotlib.pyplot as plt

# utility function u(c) = 1 - exp(-gamma*x)

# Define the function when gamma = -1
def u_1(x):
    return 1 - np.exp(x)

# Define the function when gamma = -2
def u_2(x):
    return 1 - np.exp(2*x)

# Define the function when gamma = 1
def u_3(x):
    return 1 - np.exp(-x)

# Define the function when gamma = 2
def u_4(x):
    return 1 - np.exp((-2)*x)

# Define the function when gamma = 0
def u_0(x):
    return 1 - np.exp(0*x)

# Define the x-values to plot
x = np.linspace(0.0, 0.7, 40)

# Evaluate u(x) for each x-value
y_1 = u_1(x)
y_2 = u_2(x)
y_3 = u_3(x)
y_4 = u_4(x)
y_0 = u_0(x)
# Create the plot
plt.plot(x, y_1, label = 'gamma = -1')
plt.plot(x, y_2, label = 'gamma = -2')
plt.plot(x, y_3, label = 'gamma = 1')
plt.plot(x, y_4, label = 'gamma = 2')
plt.plot(x, y_0, label = 'gamma = 0')

# Add a vertical line at x = 0 to show the y-axis
#plt.axvline(x=0, color='black', linestyle='-')

# Add labels and title
plt.xlabel('c')
plt.ylabel('u(c)')
plt.legend()
plt.title(r'Graph of $u(c) = 1 - e^{(-\gamma* c)}$ for $\gamma = -1, -2, 0, 1, 2$')

# Show the plot
plt.show()
