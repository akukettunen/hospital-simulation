from main import run_simulation, Stats
import numpy as np

# Constants
NUM_OF_PATIENTS = 20
SAMPLES = 20
SIM_TIME = 1000
SEEDS = np.random.default_rng().integers(low=0, high=10000, size=SAMPLES)
results_3p4r = [run_simulation(3, 1, 4, SIM_TIME, seed) for seed in SEEDS]
results_3p5r = [run_simulation(3, 1, 5, SIM_TIME, seed) for seed in SEEDS]
results_4p5r = [run_simulation(4, 1, 5, SIM_TIME, seed) for seed in SEEDS]
results_3p4r_noTwist = [run_simulation(3, 1, 4, SIM_TIME, seed, False) for seed in SEEDS]
results_3p5r_noTwist = [run_simulation(3, 1, 5, SIM_TIME, seed, False) for seed in SEEDS]
results_4p5r_noTwist = [run_simulation(4, 1, 5, SIM_TIME, seed, False) for seed in SEEDS]

class ValuesOfInterest:
    mean: float
    conf_ival_95_size: float

    def __init__(self, mean, conf_ival_95_size):
        self.mean = mean
        self.conf_ival_95_size = conf_ival_95_size

    def print(self):
        print(f"\tmean: {self.mean}")
        conf_min = self.mean - self.conf_ival_95_size
        conf_max = self.mean + self.conf_ival_95_size
        print(f"\t95% confidence interval: [{conf_min}, {conf_max}]")

def values(arr):
  mean = sum(arr) / SAMPLES
  # Copied straight from sample solutions
  variance = sum([(p - mean) ** 2 for p in arr]) / (SAMPLES - 1)
  std_deviation = sqrt(variance)
  c = 2.093

  return ValuesOfInterest(
    mean=mean,
    conf_ival_95_size=c * std_deviation / sqrt(SAMPLES)
  )

def analyze(samples):
    print("Probability of all recovery rooms being full:")
    values(
        [s.time_all_recovery_rooms_full / SIM_TIME for s in samples]
    ).print()
    print("Average queue length before preparation:")
    values(
        [s.prep_room_queue_length_total / SIM_TIME for s in samples]
    ).print()

def analyze_diffs(s_from, s_to):
    """Run `analyze` for the difference between two stats instances."""
    analyze([s2.difference_from(s1) for s1, s2 in zip(s_from, s_to)])

print("individual cases:")
print("\n3p4r")
analyze(results_3p4r)
print("\n3p5r")
analyze(results_3p5r)
print("\n4p5r")
analyze(results_4p5r)
print("\npairwise differences:")
print("\nfrom 3p4r to 3p5r:")
analyze_diffs(results_3p4r, results_3p5r)
print("\nfrom 3p4r to 4p5r:")
analyze_diffs(results_3p4r, results_4p5r)
print("\nfrom 3p5r to 4p5r:")
analyze_diffs(results_3p5r, results_4p5r)
print("\ndifferences between twisted and untwisted versions:")
print("\n3p4r")
analyze_diffs(results_3p4r, results_3p4r_noTwist)
print("\n3p5r")
analyze_diffs(results_3p5r, results_3p5r_noTwist)
print("\n4p5r")
analyze_diffs(results_4p5r, results_4p5r_noTwist)