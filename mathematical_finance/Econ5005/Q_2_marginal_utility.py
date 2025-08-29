import numpy as np
import matplotlib.pyplot as plt

#marginal utility function u'(c) = gamma exp(-gamma*x)

# Define the marginal utility function when gamma = 1, 
def mu_1(x):
    return  np.exp(-x)

# Define the marginal utility function when gamma = 2, 
def mu_2(x):
    return  2*np.exp(-2*x)

# Define the marginal utility function when gamma = -1, 
def mu_3(x):
    return  -np.exp(x)

# Define the marginal utility function when gamma = -2, 
def mu_4(x):
    return  -2*np.exp(2*x)

# Define the marginal utility function when gamma = 0, 
def mu_5(x):
    return  0*np.exp(0*x)

# Define the x-values to plot
x = np.linspace(0.0, 1, 40)

# Evaluate u(x) for each x-value
y_1 = mu_1(x)
y_2 = mu_2(x)
y_3 = mu_3(x)
y_4 = mu_4(x)
y_0 = mu_5(x)
# Create the plot
plt.plot(x, y_1, label = 'gamma = 1')
plt.plot(x, y_2, label = 'gamma = 2')
plt.plot(x, y_3, label = 'gamma = -1')
plt.plot(x, y_4, label = 'gamma = -2')
plt.plot(x, y_0, label = 'gamma = 0')

# Add labels and title
plt.xlabel('c')
plt.ylabel('u\'(c)')
plt.legend()
plt.title(r'Graph of $u(c) = \gamma e^{(-\gamma c)}$ for $\gamma = -1, -2, 0, 1, 2$')

# Show the plot
plt.show()
