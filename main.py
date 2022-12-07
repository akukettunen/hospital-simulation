import simpy
import numpy as np
from math import sqrt

DEATH_PROBS = .02

class Stats:
    patient_count = 0
    dead_patients = 0
    time_all_recovery_rooms_full = 0
    prep_room_queue_length_total = 0
    prep_queue_arr = []
    patient_lifetime_total = 0

    def difference_from(self, other):
        diff = Stats()
        diff.time_all_recovery_rooms_full = (
            self.time_all_recovery_rooms_full - other.time_all_recovery_rooms_full
        )
        diff.patient_lifetime_total = (
            self.patient_lifetime_total - other.patient_lifetime_total
        )
        diff.patient_count = self.patient_count - other.patient_count
        diff.dead_patients = self.dead_patients - other.dead_patients
        diff.prep_room_queue_length_total = (
            self.prep_room_queue_length_total - other.prep_room_queue_length_total
        )

        return diff

def run_simulation(
        prep_capacity,
        oper_capacity,
        reco_capacity,
        run_time,
        seed,
        interarrival_t,
        prep_t,
        rec_t,
        twist = True
    ):
    env = simpy.Environment()
    prep_rooms = simpy.Resource(env, capacity=prep_capacity)
    oper_rooms = simpy.Resource(env, capacity=oper_capacity)
    reco_rooms = simpy.Resource(env, capacity=reco_capacity)
    rng = np.random.default_rng(seed=seed)
    stats = Stats()

    # Add stats
    # for t in range(1, run_time):
        # env.run(until=t)

    def patient(env, prep_rooms, operating_rooms, recovery_rooms, stats, prep_t, rec_t):
        def prep_dur():
            if prep_t: 
                return prep_t
            return rng.exponential(scale=40)
        
        def oper_dur():
            return rng.exponential(scale=20)
        
        def reco_dur():
            if rec_t:
                return rec_t
            return rng.exponential(scale=40)
        
        def death_dur():
            return 20

        # keep track of time for statistics purposes
        start_time = env.now

        # No need to loop cause not redoing operations
        # Prep
        in_prep_room = prep_rooms.request()
        yield in_prep_room
        yield env.timeout(prep_dur())

        # Operation
        in_op_room = operating_rooms.request()
        yield in_op_room
        prep_rooms.release(in_prep_room)
        yield env.timeout(oper_dur())

        died = False
        # Death?
        if twist and rng.random() < DEATH_PROBS:
            stats.dead_patients += 1
            died = True
            yield env.timeout(death_dur())

        # Recovery
        if not died:
            in_rec_room = recovery_rooms.request()
            yield in_rec_room
            operating_rooms.release(in_op_room)
            yield env.timeout(reco_dur())
            recovery_rooms.release(in_rec_room)

        duration = env.now - start_time
        stats.patient_lifetime_total += duration
        stats.patient_count += 1
    
    def patient_flow(env, prep_rooms, operating_rooms, recovery_rooms, stats):
        def inter_arrival_delay():
            if interarrival_t:
                return interarrival_t

            scale = 25
            return rng.exponential(scale=scale)

        while True:
            env.process( patient(env, prep_rooms, operating_rooms, recovery_rooms, stats, prep_t, rec_t) )
            yield env.timeout(inter_arrival_delay())

    env.process(patient_flow(env, prep_rooms, oper_rooms, reco_rooms, stats))

    # run the simulation loop manually to be able to inspect state
    for t in range(1, run_time):
        env.run(until=t)

        stats.prep_room_queue_length_total += len(prep_rooms.queue)
        stats.prep_queue_arr.append(len(prep_rooms.queue))

        if reco_rooms.count == reco_rooms.capacity:
            stats.time_all_recovery_rooms_full += 1

    return stats

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