# dsnd-probability-tl2024 package

Package includes a Gaussian and Binomial class for calculating and visualizing a Gaussian and Binomial distributions respectively. 

# Files
    1. Generaldistribution.py 
        a.  Parent class
    2. Binomialdistribution.py
        a. Contains Binomial class
    3. Gaussiandistribution.py
        a. Contains Gassian class

# installation
### pip install dsnd-probabilitytl2024

# import the distribution
### from dsnd-probability-tl2024 import Gaussian, Binomail

# Instantiate Guassian Object
    1. g_instance = Gaussian(10,7)
    2. g_instance.data = [1, 3, 99, 100, 120, 32, 330, 23, 76, 44, 31]
    3. g_instance.calculate_mean()
    4. g_instance.calculate_stdev()
    5. g_instance.pdf(25)
    6. g_instance.plot_histogram()
    7. g_instance.plot_histogram_pdf()

# Instantiate Binomial Object
    1. b_instance1 = Binomial(.4,25)
    2. b_instance.data1 = [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0]
    3. b_instance1.calculate_mean()
    4. b_instance1.calculate_stdev()
    5. b_instance1.pdf(5)
    6. b_instance1.plot_bar_pdf()
    7. b_instance2_ = Binomial(.4, 60)
    8. binomial_sum = b_instance1 + b_instance2
    9. print(binomial_sum)