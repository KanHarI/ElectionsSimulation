
import numpy as np

# Ratios based on random internet polls. updated at 2019-01-18
CANDIDATES = {
    "LIKUD": 33,
    "YESH_ATID": 13,
    "HOSEN_LEYISRAEL": 13,
    "HAMESHUTEFET": 12,
    "HAYAMIN_HAHADASH": 8,
    "HAAVODA": 8,
    "YAHADUT_HATORA": 8,
    "YISRAEL_BEITENU": 5,
    "KULANU": 5,
    "SHAS": 5,
    "MERETZ": 5,
    "GESHER": 5,
    "HABAIT_HAYEHUDI": 4,
    "HATNUA": 3,
    "SURPRISE": 2, # ZEHUT\ALE_YAROK\etc.
    "PETEK_LAVAN": 3,
    None: 36, # non-voting. based upon voting percent in 2013&2015
}

# Speculation
SURPLUS_AGREEMENT = [
    ("LIKUD", "HAYAMIN_HAHADASH"),
    ("YESH_ATID", "HOSEN_LEYISRAEL"),
    ("HAAVODA", "MERETZ"),
    ("YAHADUT_HATORA", "SHAS"),
    ("YISRAEL_BEITENU", "HABAIT_HAYEHUDI"),
    ("KULANU", "GESHER"),
    ("HAMESHUTEFET",),
    ("HATNUA",),
    ("SURPRISE",),
]

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


# Number based upon linear trend from 2013&2015 elections
NUM_LEGAL_VOTERS = 5500000
AHUZ_HAHASIMA = 4
NUM_MANDATES = 120

class Simulation:
    def __init__(self):
        self.base_dist = {i: float(j) for i, j in CANDIDATES.items()}
        self.distribution = None
        self._sample = None

    def random_drift(self, constant_variance, relative_variance):
        constant_drift = np.random.normal(0.0, constant_variance, (len(self.base_dist),))
        relative_drift = np.random.normal(0.0, relative_variance, (len(self.base_dist),))
        self.distribution = dict()
        for i, key in enumerate(self.base_dist.keys()):
            self.distribution[key] = max(self.base_dist[key]*np.exp(relative_drift[i]) + constant_drift[i], 0)
        return self.distribution

    def sample(self, num_voters):
        if self.distribution is None:
            print("""Warning: sampling without drift!
                     this can lead into weired behaviours as voters distribution is alligned
                     to polling resolution of a single knesset member""")
            self.distribution = self.base_dist
        pvals = []
        for i, key in enumerate(self.distribution.keys()):
            pvals.append(self.distribution[key])
        pvals = np.array(pvals)
        pvals /= np.sum(pvals)
        result = np.random.multinomial(NUM_LEGAL_VOTERS, pvals, 1)[0]
        result = result[:KEY_TO_I[None]]
        self._sample = result
        return result

    def mandates(self):
        if self.sample is None:
            raise Exception("Cannot distribute mandes without sampling voters!")
        mandates = self._sample/np.sum(self._sample)*NUM_MANDATES
        mandates = mandates.astype(np.int16)
        mandates = mandates * (mandates >= AHUZ_HAHASIMA)
        mandates = mandates[:KEY_TO_I["PETEK_LAVAN"]]
        surplus_matrix = SURPLUS_MATRIX
        surplus_matrix = (surplus_matrix.T * (mandates > 0)).T

        # Bader-offer
        spare_mandates = NUM_MANDATES - np.sum(mandates)
        jointvoters = self._sample[:KEY_TO_I["PETEK_LAVAN"]].dot(surplus_matrix)
        for mandate in range(spare_mandates):
            jointmandates = mandates.dot(surplus_matrix)
            jointcost = jointvoters/(jointmandates+1)
            idx = np.nonzero(surplus_matrix[:,np.argmax(jointcost)])[0]
            individual_cost = self._sample[idx]/(mandates[idx] + 1)
            mandates[idx[np.argmax(individual_cost)]] += 1

        return mandates

NUM_RUNS = 1000000

def main():
    d = Simulation()
    affected = {key: 0 for key in CANDIDATES.keys()}
    affected_weighted = {key: 0 for key in CANDIDATES.keys()}
    for i in range(NUM_RUNS):
        d.random_drift(1, 0.2)
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
        if i % 10000 == 0:
            print(i)
            _affected = {key:(0 if val==0 else i/val) for key, val in affected.items()}
            print("Affect chance - 1 in:")
            print(_affected)
            print("Expected value of voting - 1 in:")
            _affected_weighted = {key:(0 if val==0 else i/val) for key, val in affected_weighted.items()}
            print(_affected_weighted)
            print("\n\n")
    print("\n\n\nFinal - the chance of affecting result, multiplying by num of knesset members changed is:")
    _affected = {key:(0 if val==0 else NUM_RUNS/val) for key, val in affected.items()}
    _affected_weighted = {key:(0 if val==0 else NUM_RUNS/val) for key, val in affected_weighted.items()}
    print(_affected)
    print("\n\n\nAnd w.r.t. num of knesset member changed:")
    print(_affected_weighted)
    return 0

if __name__ == "__main__":
    exit(main())
