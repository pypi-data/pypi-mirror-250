import math
from math import factorial as fact
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials
            
    """
    
    '''
          A binomial distribution is defined by two variables: 
              the probability of getting a positive outcome
              the number of trials
    
          If you know these two values, you can calculate the mean and the standard deviation
          
          For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
          You can then calculate the mean and standard deviation with the following formula:
              mean = p * n
              standard deviation = sqrt(n * p * (1 - p))
    '''
    
    def __init__(self, prob=.5, size=20):
        self.p = prob
        self.n = size

        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())

    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
                
        self.mean = self.p * self.n
        return self.mean


    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
                
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))        
        return self.stdev

        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """        
        
        self.n = len(self.data)
        self.p = sum(self.data)/self.n
        # self.p = self.data.count(1)/self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        
        return self.p, self.n

        
    def generate_barchart(self, x, y, title, x_label, y_label):
        """Helper function to generate a bar chart with a title and axis labels.
        
        Args:
            None
            
        Returns:
            None
        """

        plt.bar(x, y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        zeros = self.data.count(0)
        ones = self.data.count(1)
        x_axis = [0, 1]
        y_axis = [zeros, ones]
        
        title = "Trial frequencies"
        xlabel = "Outcome"
        ylabel = "Frequency"
        self.generate_barchart(x_axis, y_axis, title, xlabel, ylabel)

        plt.show()

        
    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        negative_outcomes = self.n - k
        n_choose_k = fact(self.n) / (fact(k)*fact(negative_outcomes))
        probability_part = self.p**k * (1-self.p)**(negative_outcomes)
        
        return n_choose_k * probability_part


    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        
        k = list(range(self.n))
        pdf = [self.pdf(val) for val in k]
        title = "PDF of binomial distribution of k"
        xlabel = "Data"
        ylabel = "PDF"
        self.generate_barchart(k, pdf, title, xlabel, ylabel)
        plt.show()
        
        return k, pdf
        
                
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        '''
        The formula for summing two binomial distributions with different p values 
        is more complicated, so this function implements the case for two 
        distributions with equal p.
        
        the try, except statement above will raise an exception if the p values are not equal
        
          When adding two binomial distributions, the p value remains the same
          The new n value is the sum of the n values of the two distributions.
        '''

        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        result.calculate_mean()
        result.calculate_stdev()
        
        return result
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
    
        output = "mean " + str(self.mean) + \
        ", standard deviation " + str(self.stdev) + \
        ", p " + str(self.p) + \
        ", n " + str(self.n)
        
        return output
