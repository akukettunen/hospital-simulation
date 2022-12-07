import main
import numpy as np
import randomize
import stats
import math

"""
Experiments:
    interarrival_time   prep_time   rec_time    prep_rooms  rec_rooms
1.      exp(25)          exp(40)     exp(40)        4           5
2.      exp(25)        unif(30,50) unif(30, 50)     4           5
3.    unif(20,30)        exp(40)     exp(40)        4           5
4.    unif(20,30)      unif(30, 50) unif(30, 50)    4           5
5.     exp(22.5)         exp(40)     exp(40)        4           5
6.     exp(22.5)       unif(30, 50) unif(30, 50)    4           5
7.    unif(20, 25)       exp(40)     exp(40)        4           5
8.    unif(20, 25)     unif(30, 50) unif(30, 50)    4           5
"""

SIM_LENGTH= 1_000

sims = [
    # 1.      exp(25)          exp(40)     exp(40)
    {
        "interarrival_t": {
            "exp": True,
            "val": 25
        },
        "prep_t": {
            "exp": True,
            "val": 40
        },
        "rec_t": {
            "exp": True,
            "val": 40
        }
    },
    # 2.      exp(25)        unif(30,50) unif(30, 50)
    {
        "interarrival_t": {
            "exp": True,
            "val": 25
        },
        "prep_t": {
            "exp": False,
            "val": [30, 50]
        },
        "rec_t": {
            "exp": False,
            "val": [30, 50]
        }
    },
    # 3.    unif(20,30)        exp(40)     exp(40)
    {
        "interarrival_t": {
            "exp": False,
            "val": [20, 30]
        },
        "prep_t": {
            "exp": True,
            "val": 40
        },
        "rec_t": {
            "exp": True,
            "val": 40
        }
    },
    # 4.    unif(20,30)      unif(30, 50) unif(30, 50)    4           5
    {
        "interarrival_t": {
            "exp": False,
            "val": [20, 30]
        },
        "prep_t": {
            "exp": False,
            "val": [30, 50]
        },
        "rec_t": {
            "exp": False,
            "val": [30, 50]
        }
    },
    # 5.     exp(22.5)         exp(40)     exp(40)        4           5
    {
        "interarrival_t": {
            "exp": True,
            "val": 22.5
        },
        "prep_t": {
            "exp": True,
            "val": 40
        },
        "rec_t": {
            "exp": True,
            "val": 40
        }
    },
    # 6.     exp(22.5)       unif(30, 50) unif(30, 50)    4           5
    {
        "interarrival_t": {
            "exp": True,
            "val": 22.5
        },
        "prep_t": {
            "exp": False,
            "val": [30, 50]
        },
        "rec_t": {
            "exp": False,
            "val": [30, 50]
        }
    },
    # 7.    unif(20, 25)       exp(40)     exp(40)        4           5
    {
        "interarrival_t": {
            "exp": False,
            "val": [20, 25]
        },
        "prep_t": {
            "exp": True,
            "val": 40
        },
        "rec_t": {
            "exp": True,
            "val": 40
        }
    },
    # 8.    unif(20, 25)     unif(30, 50) unif(30, 50)    4           5
    {
        "interarrival_t": {
            "exp": False,
            "val": [20, 25]
        },
        "prep_t": {
            "exp": False,
            "val": [30, 50]
        },
        "rec_t": {
            "exp": False,
            "val": [30, 50]
        }
    },
]

experiments = []

for i, sim in enumerate(sims):
    experiment = []
    for k in range(1, 11):
        if sim["interarrival_t"]["exp"]:
            interarrival_time = randomize.exponential(sim["interarrival_t"]["val"])
        else:
            interarrival_time = randomize.unif(sim["interarrival_t"]["val"])

        if sim["prep_t"]["exp"]:
            prep_time = randomize.exponential(sim["prep_t"]["val"])
        else:
            prep_time = randomize.unif(sim["prep_t"]["val"])

        if sim["rec_t"]["exp"]:
            rec_time = randomize.exponential(sim["rec_t"]["val"])
        else:
            rec_time = randomize.unif(sim["rec_t"]["val"])

        result = main.run_simulation(3, 1, 5, SIM_LENGTH, k, interarrival_time, prep_time, rec_time, False)
        experiment = experiment + [result.prep_queue_arr]

    experiments = experiments + [experiment]

#TODO: safeguard against going over simulation limits with sample or interval sizes
sampleLength = 50
sampleCount = 10
interval = 50
for simulationSet in experiments:
    for experiment in simulationSet:
        sampleList = []
        for i in range(0,sampleCount):
            sampleList = sampleList + [experiment[0+i*2*interval:sampleLength+i*2*sampleLength]]

        sampleMeans = []
        for i in range(0,sampleCount):
            sampleMeans = sampleMeans + [stats.mean(sampleList[i])]

        covariances = []
        for i in range(1, sampleCount):
            covariance = 0
            X1 = sampleList[i-1]  #list of values in the first sample
            X2 = sampleList[i]    #list of values in the second sample
            u1 = sampleMeans[i-1] #mean of the first sample
            u2 = sampleMeans[i]   #mean of the second sample
            for index in range(0,sampleLength):
                covariance += ((X1[index] - u1)*(X2[index] - u2)) / sampleLength
            covariances = covariances + [covariance]

        correlations = []
        for i in range(1,sampleCount):
            X1_variance = stats.variance(sampleList[i-1])
            X2_variance = stats.variance(sampleList[i])
            try:
                correlation = covariances[i-1]/math.sqrt(X1_variance*X2_variance)
                correlations = correlations + [correlation]
            except:
                correlations = correlations + [0]        

        print("Correlations:")
        print("------------")
        print(correlations)