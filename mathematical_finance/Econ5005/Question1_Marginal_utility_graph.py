import numpy as np
import matplotlib.pyplot as plt

# marginal utility function f'(k) = alpha* k^(alpha -1)

# Define the marginal utility function when alpha = 3, 
def u_1(x):
    return  3*(x**2)

# Define the marginal utility function when alpha = 2, 
def u_2(x):
    return  2*(x**1)

# Define the marginal utility function when alpha = 1.5, 
def u_3(x):
    return  1.5*(x**0.5)

# Define the marginal utility function when alpha = 1.0, 
def u_4(x):
    return  1.0*(x**0.0)

# Define the marginal utility function when alpha = 0.5, 
def u_5(x):
    return  0.5*(x**(-0.5))

# Define the marginal utility function when alpha = 0.0, 
def u_6(x):
    return  0.0*(x**(-1.0))

# Define the marginal utility function when alpha = -0.05, 
def u_7(x):
    return  -0.5*(x**(-1.1))

# Define the x-values to plot
x = np.linspace(0.0, 1.5, 20)

# Evaluate u(x) for each x-value
y_1 = u_1(x)
y_2 = u_2(x)
y_3 = u_3(x)
y_4 = u_4(x)
y_5 = u_5(x)
y_6 = u_6(x)
y_7 = u_7(x)
# Create the plot
plt.plot(x, y_1, label = 'alpha = 3')
plt.plot(x, y_2, label = 'alpha = 2')
plt.plot(x, y_3, label = 'alpha = 1.5')
plt.plot(x, y_4, label = 'alpha = 1')
plt.plot(x, y_5, label = 'alpha = 0.5')
plt.plot(x, y_6, label = 'alpha = 0.0')
plt.plot(x, y_7, label = 'alpha = -0.1')


# Add annotations for each line
plt.text(1.5, u_1(1.5), 'alpha = 3', verticalalignment='bottom')
plt.text(1.5, u_2(1.5), 'alpha = 2', verticalalignment='bottom')
plt.text(1.5, u_3(1.5), 'alpha = 1.5', verticalalignment='bottom')
plt.text(1.5, u_4(1.5), 'alpha = 1', verticalalignment='bottom')
plt.text(1.5, u_5(1.5), 'alpha = 0.5', verticalalignment='bottom')
plt.text(1.5, u_6(1.5), 'alpha = 0.0', verticalalignment='bottom')
plt.text(1.5, u_7(1.5), 'alpha = -0.1', verticalalignment='bottom')

# Add labels and title
plt.xlabel('k')
plt.ylabel(r'$f\'(k) = \alpha k^{\alpha - 1}$')
plt.legend()
plt.title(r'Graph of $f\'(k) = \alpha k^{\alpha - 1}$ for $\alpha =  -0.5, 0, 0.5, 1, 1.5,2, 3$')

# Show the plot
plt.show()
