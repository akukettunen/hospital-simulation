# -*- coding: utf-8 -*-


import random

# returns the exponentially distributed random number of desired mean
def exponential(mean):
    lambd = 1.0 / mean
    return random.expovariate(lambd)

# returns the uniformly distributed random number of desired range
def unif(arr):
    return random.uniform(arr[0], arr[1])



