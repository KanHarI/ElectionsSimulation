
import numpy as np
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


AHUZ_HAHASIMA = 4
NUM_MANDATES = 120

class Simulation:
    def __init__(self, constant_variance, relative_variance):
        self.base_dist = {i: float(j) for i, j in CANDIDATES.items()}
        self.constant_variance = constant_variance
        self.relative_variance = relative_variance
        self.distribution = None
        self._sample = None

    def random_drift(self):
        constant_drift = np.random.normal(0.0, self.constant_variance, (len(self.base_dist),))
        relative_drift = np.random.normal(0.0, self.relative_variance, (len(self.base_dist),))
        self.distribution = dict()
        for i, key in enumerate(self.base_dist.keys()):
            self.distribution[key] = max(self.base_dist[key]*np.exp(relative_drift[i]) + constant_drift[i], 0)
        return self.distribution

    def sample(self, num_voters):
        if self.distribution is None:
            print("""\n\nWarning: sampling without drift!
this can lead into weired behaviours as voters distribution is alligned
to polling resolution of a single knesset member.\n\n""")
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
