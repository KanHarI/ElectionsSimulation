
import argparse
import numpy as np

from simulation import Simulation

from constants import DEFAULT_NUM_ITERATIONS, DEFAULT_PRINT_INTERVAL, DEFAULT_CONSTANT_DRIFT, DEFAULT_RELATIVE_DRIFT
from configuration import NUM_LEGAL_VOTERS, CANDIDATES, SURPLUS_AGREEMENT


I_TO_KEY = dict()
KEY_TO_I = dict()
for i, key in enumerate(CANDIDATES.keys()):
    I_TO_KEY[i] = key
    KEY_TO_I[key] = i

SURPLUS_AGREEMENT_I = list()
for item in SURPLUS_AGREEMENT:
    SURPLUS_AGREEMENT_I.append(tuple(map(lambda x: KEY_TO_I[x], item)))

SURPLUS_MATRIX = np.zeros((len(CANDIDATES)-2, len(SURPLUS_AGREEMENT)), dtype=np.int16)
for i in range(len(SURPLUS_AGREEMENT_I)):
    for j in SURPLUS_AGREEMENT_I[i]:
        SURPLUS_MATRIX[j,i] = 1



def main(args):
    d = Simulation(args.constant_drift, args.relative_drift)
    affected = {key: 0 for key in CANDIDATES.keys()}
    affected_weighted = {key: 0 for key in CANDIDATES.keys()}
    for i in range(args.num_iterations):
        if not (args.disable_drift):
            d.random_drift()
        d.sample(NUM_LEGAL_VOTERS)
        mandates = d.mandates()
        for key in CANDIDATES.keys():
            if key == None:
                continue # Non-voters are not part of the results
            d._sample[KEY_TO_I[key]] += 1
            delta = np.sum(np.abs(mandates - d.mandates()))
            if delta:
                affected[key] += 1
                affected_weighted[key] += delta
            d._sample[KEY_TO_I[key]] -= 1
        if i % args.print_interval == 0:
            print(i)
            _affected = {key:(0 if val==0 else i/val) for key, val in affected.items()}
            print("Affect chance - 1 in:")
            print(_affected)
            print("Expected value of voting in mandates:")
            _affected_weighted = {key:(0 if val==0 else val/i) for key, val in affected_weighted.items()}
            print(_affected_weighted)
            print("\n\n")
    print("\n\n\nFinal - the chance of affecting result:")
    _affected = {key:(0 if val==0 else NUM_RUNS/val) for key, val in affected.items()}
    _affected_weighted = {key:(0 if val==0 else val/NUM_RUNS) for key, val in affected_weighted.items()}
    print(_affected)
    print("\n\n\nVoting utility in mandates:")
    print(_affected_weighted)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-iterations", type=int, default=DEFAULT_NUM_ITERATIONS,
        help="Number of simulation iterations. Defualt: {0}".format(DEFAULT_NUM_ITERATIONS))
    parser.add_argument("--print-interval", type=int, default=DEFAULT_PRINT_INTERVAL,
        help="Print aggregated information once in this many iterations. Defualt: {0}".format(DEFAULT_PRINT_INTERVAL))
    parser.add_argument("--disable-drift", action="store_true",
        help="Without this parameter, random drift will be applied to voting percets of each party in each iteration")
    parser.add_argument("--constant-drift", type=float, default=DEFAULT_CONSTANT_DRIFT,
        help="The standard diviation of a random value added to or substracted from the"+\
            " percent of voters voting for each party. Defualt: {0}".format(DEFAULT_CONSTANT_DRIFT))
    parser.add_argument("--relative-drift", type=float, default=DEFAULT_RELATIVE_DRIFT,
        help="The standard diviation of a random value added to or substracted from the"+\
        " percent of voters voting for each party, in a logarithmic scale. Defualt: {0}".format(DEFAULT_RELATIVE_DRIFT))
    args = parser.parse_args()
    exit(main(args))

