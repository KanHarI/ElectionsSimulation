
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
    None: 36, # non-voting. based upon voting percent in 2013&2015
}

I_TO_KEY = dict()
KEY_TO_I = dict()
for i, key in enumerate(CANDIDATES.keys()):
    I_TO_KEY[i] = key
    KEY_TO_I[key] = i


# Number based upon linear trend from 2013&2015 elections
NUM_LEGAL_VOTERS = 5500000
AHUZ_HAHASIMA = 4

class Simulation:
    def __init__(self):
        self.base_dist = {i: float(j) for i, j in CANDIDATES.items()}
        self.distribution = None
        self.sample = None

    def random_drift(self, constant_variance, relative_variance):
        constant_drift = np.random.normal(0.0, constant_variance, (len(self.base_dist),))
        relative_drift = np.random.normal(0.0, relative_variance, (len(self.base_dist),))
        self.distribution = dict()
        for i, key in enumerate(self.base_dist.keys()):
            self.distribution[key] = max(self.base_dist[key]*np.exp(relative_drift[i]) + constant_drift[i], 0)

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
        self.sample = result
        return result

    def mandates(self):
        if self.sample is None:
            raise Exception("Cannot distribute mandes without sampling voters!")
        mandates = self.sample/np.sum(self.sample)

def main():
    d = Distribution()
    d.random_drift(1.5, 0.3)
    print(d.sample(NUM_LEGAL_VOTERS))
    return 0

if __name__ == "__main__":
    exit(main())