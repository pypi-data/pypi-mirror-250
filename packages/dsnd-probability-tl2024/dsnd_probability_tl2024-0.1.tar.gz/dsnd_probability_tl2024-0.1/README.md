# dsnd-probability-tl2024 package

Package includes a Gaussian and Binomial class for calculating and visualizing a Gaussian and Binomial distributions respectively. 

# Files
    1.Generaldistribution.py 
        1.  Parent class
    2. Binomialdistribution.py
        1. Contains Binomial class
    3. Gaussiandistribution.py
        1. Contains Gassian class

# installation
### pip install dsnd-probabilitytl2024

# import the distribution
### from dsnd-probability-tl2024 import Gaussian, Binomail

# Instantiate Guassian Object
### g_instance = Gaussian(10,7)
### g_instance.data = [1, 3, 99, 100, 120, 32, 330, 23, 76, 44, 31]
### g_instance.calculate_mean()
### g_instance.calculate.stdev()
### g_instance.pdf(25)
### g_instance.plot_histogram()
### g_instance.plot_histogram_pdf()

# Instantiate Binomial Object
### b_instance1 = Binomial(.4,25)
### b_instance.data1 = [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0]
### b_instance1.calculate_mean()
### b_instance1.calculate.stdev()
### b_instance1.pdf(5)
### b_instance1.plot_bar_pdf()
### b_instance2_ = Binomial(.4, 60)
### binomial_sum = b_instance1_ + b_instance2
### print(binomial_sum)