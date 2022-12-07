# -*- coding: utf-8 -*-

import math

def mean(values):
    """
    Calculates the mean of the given values with given weigths. 
    """
    sum = 0
    for value in values:
        sum += value

    if not len(values):
        return 0
        
    return sum / len(values)

def standard_deviation(values):
    """
    Calculates the standard deviation of the given values.
    """
    average = mean(values)
    sum = 0
    for value in values:
        difference = value - average
        sum += pow(difference, 2)
    #Should this be considered variance or sample variance?
    variance = sum/len(values)
    return math.sqrt(variance)

def confidence95(values):
    """
    Calculates confidence interval for 95% confidence level given the values
    """
    n = len(values)
    x = mean(values)
    s = standard_deviation(values)
    z = 1.96
    return (x-z*(s/math.sqrt(n)), x+z*(s/math.sqrt(n)))

def sum(values):
    if len(values) > 0:
        return values[0] + sum(values[1:])
    else:
        return 0

def variance(values):
    average = mean(values)
    sum = 0
    for value in values:
        difference = value - average
        sum += pow(difference, 2)
    #Should this be considered variance or sample variance?
    variance = sum/len(values)
    return variance

#def covariance(sample1, sample2):

