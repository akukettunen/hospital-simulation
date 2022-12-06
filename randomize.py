# -*- coding: utf-8 -*-


import random

# returns the exponentially distributed random number of desired mean
def exponential(mean):
    lambd = 1.0 / mean
    return random.expovariate(lambd)

# returns the uniformly distributed random number of desired range
def unif(a, b):
    return random.uniform(a,b)



