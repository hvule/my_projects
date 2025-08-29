import numpy as np
import matplotlib.pyplot as plt
import pylatexenc
from sympy import latex
#inverse of derivative  u'^{-1}(xi) = -ln(xi/gamma)/gamma

# Define the inverse of marginal utility when gamma = 1, 
def imu_1(x):
    return  -np.log(x)

# Define the inverse of marginal utility when gamma = 2, 
def imu_2(x):
    return  -np.log(x/2)/2

# Define the inverse of marginal utility when gamma = -1, 
def imu_3(x):
    return  np.log(-x)

# Define the inverse of marginal utility when gamma = -2, 
def imu_4(x):
    return  np.log(-x/2)/2

# Define the inverse of marginal utility when gamma = 1/2, 
def imu_5(x):
    return  -2 *np.log(2*x)

# Define the inverse of marginal utility when gamma = -1/2, 
def imu_6(x):
    return  2 *np.log(-2*x)

# Define the x-values positive to plot 
x1 = np.linspace(0.0, 3, 40)

# Define the x-values positive to plot 
x2 = np.linspace(-10, 0.0, 50)

# Evaluate u(x) for each x-value positive
y_1 = imu_1(x1)
y_2 = imu_2(x1)
y_5 = imu_5(x1)

# Evaluate u(x) for each x-value negative
y_3 = imu_3(x2)
y_4 = imu_4(x2)
y_6 = imu_6(x2)



#Create the plot

plt.plot(x2, y_3, label = 'gamma = -1')
plt.plot(x2, y_4, label = 'gamma = -2')
plt.plot(x2, y_6, label = 'gamma = -0.5')


# Add a horizontal line at y = 0 to show the x-axis
plt.axhline(y=0, color='black', linestyle='-') 



# Add labels and title
plt.xlabel(r'$\xi$')
plt.ylabel(r'$u^{-1}\' (\xi)$')
plt.legend()
#plt.title(r'Graph of $u^{-1}\' (\xi) = -\dfrac{ln(\xi) - ln(\gamma)}{\gamma}$ for $\gamma = 1, 2, 0.5$')
plt.title(r'Graph of $u^{-1}\' (\xi) = -\dfrac{ln(\xi) - ln(\gamma)}{\gamma}$ for $\gamma = -1, -2, -0.5$')

# Show the plot
plt.show()
