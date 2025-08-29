import numpy as np
import matplotlib.pyplot as plt

#utility function f(k) = k^alpha

# Define the  utility function when alpha = 2, 
def u_1(x):
    return  x**2

# Define the  utility function when alpha = 1, 
def u_2(x):
    return  x**1

# Define the  utility function when alpha = 0, 

def u_3(x):
    return  x**0

# Define the  utility function when alpha = 0.5, 

def u_4(x):
    return  x**0.5

# Define the  utility function when alpha = -1, 

def u_5(x):
    return  x**-0.5



# Define the x-values to plot
x = np.linspace(0.0, 2.0, 30)

# Evaluate u(x) for each x-value
y_1 = u_1(x)
y_2 = u_2(x)
y_3 = u_3(x)
y_4 = u_4(x)
y_5 = u_5(x)


# Create the plot
plt.plot(x, y_1, label = 'alpha = 2')
plt.plot(x, y_2, label = 'alpha = 1')
plt.plot(x, y_3, label = 'alpha = 0')
plt.plot(x, y_4, label = 'alpha = 1/2')
plt.plot(x, y_5, label = 'alpha = -0.5')


# Add annotations for each line
plt.text(2, u_1(2), 'alpha = 2', verticalalignment='bottom')
plt.text(2, u_2(2), 'alpha = 1', verticalalignment='bottom')
plt.text(2, u_3(2), 'alpha = 0', verticalalignment='bottom')
plt.text(2, u_4(2), 'alpha = 0.5', verticalalignment='bottom')
plt.text(2, u_5(2), 'alpha = -0.5', verticalalignment='bottom')



# Add labels and title
plt.xlabel('k')
plt.ylabel(r'$f(k) = k^\alpha$')
plt.legend()
plt.title(r'Graph of $f(k) = k^{\alpha}$ for $\alpha =  -0.5, 0, 1/2, 1, 2$')

# Show the plot
plt.show()
