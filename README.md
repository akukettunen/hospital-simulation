Interarrival times can be either exponentially or uniformly distributed with two different possible average arrival rates (exp(25) or exp (22.5),  Unif(20,30) 
or Unif(20,25))

Preparation time can be either exp(40) or Unif(30,50)

Recovery time can be either exp(40) or Unif(30,50)

There can be either 4 or 5 preparation units

There can be either 4 or 5 recovery units

For the operation, we assume exp(20) duration in all scenarios (it will be harder to influence to the process of operation and to surprises (large variance) 
involved).

In addition, you may have a suitable meaningful twist to the problem that adds yet another feature to be varied. If so, feel free to replace one of the above 
factors with you own one.

The overall goal is to ensure high utilization rate of the operation unit with reasonable amount of auxiliary facilities and without unnecessary waiting. This
means that we are dealing with queuing systems with high utilization rates and build-up of queues cannot be avoided. These in their turn introduce serial 
correlation to the system (long queue now predicts long queue in the near future).

It will be important to analyze the serial correlation and building up of the equilibrium to ensure reliable results. Select one configuration of the system 
that you think is likely to show serial correlation. Test serial correlation for this scenario. To do this you can run several (say 10) independent simulation runs 
taking several (say 10 again) samples (keeping the order is important here). By this way, you get 10 samples of independent time series and you should compute the 
correlations between the elements of these series. Observe the average length of the queue on arrival (i.e before preparation) as this queue forms a memory 
between samples that are taken too close to each other. Adjust the sample lengths and intervals between the samples to control the correlation between 
successive samples.

As for the comparison between different configurations: With the above specifications, there would be 64 different combinations to test all possible combinations. 
Construct a design of 8 experiments (using 2^(6-3)) design to identify the effects of the six structural variants.

Run the series of experiments based on the constructed design. Report the average length of the queue at the entrance.

Build a regression model for the average queue length. Which structural parameters affect the queue length significantly? Does the model make any sense (or are 
joint effects essential to take in to account in the model)?

## TL;DR: what to do!
Select i dont know