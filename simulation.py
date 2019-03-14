
import numpy as np

class Simulation:
    def __init__(self, conf):
        # Create basic support fractions of different parties
        self.base_dist = np.array([float(conf.candidates_support[conf.i_to_key[i]]) \
            for i in range(len(conf.candidates_support.keys()))], dtype=np.float)
        
        # Renormalize (Sum to 1)
        self.base_dist /= np.sum(self.base_dist)
        self.constant_variance = conf.constant_drift
        self.relative_variance = conf.relative_drift
        self.threshold = conf.threshold
        self.num_mandates = conf.num_mandates
        self.surplus_matrix = conf.surplus_matrix
        self.distribution = None
        self._sample = None

    def random_drift(self):
        constant_drift = np.random.normal(0.0, self.constant_variance, (self.base_dist.shape[0],))
        relative_drift = np.random.normal(0.0, self.relative_variance, (self.base_dist.shape[0],))
        self.distribution = np.maximum(self.base_dist*np.exp(relative_drift) + constant_drift, 0)
        
        if np.sum(self.distribution[:-1]) == 0:
            # Rarely, the whole distribution can become negative due to noise
            # we solve those cases by retrying the random drift...
            return self.random_drift()
        
        self.distribution /= np.sum(self.distribution)
        return self.distribution

    def sample(self, num_voters):
        if self.distribution is None:
            self.distribution = self.base_dist
        
        # Get a multinomial distribution sample of votes
        _result = np.random.multinomial(num_voters, self.distribution, 1)[0]

        # Remove illegal votes and non-voters
        result = _result[:-1]
        self._sample = result
        return result

    def mandates(self):
        if self.sample is None:
            raise Exception("Cannot distribute mandes without sampling voters!")
        
        # Find support fraction for every party
        mandates = self._sample/np.sum(self._sample)
        
        # Apply threshold
        threshold_sample = self._sample * (mandates > self.threshold)
        mandates *= (mandates > self.threshold)

        # Renormalize distribution after removing below-threshold parties
        mandates /= np.sum(mandates)
        
        # Distribute mandates
        mandates = mandates*self.num_mandates
        mandates = mandates.astype(np.int16)

        # The Bader-Offer algorithm
        # Number of spare mandates to split between candidates
        spare_mandates = self.num_mandates - np.sum(mandates)

        # Find the number of voters for both parties together
        # exclude voters for parties under the threshold
        jointvoters = threshold_sample.dot(self.surplus_matrix)
        for mandate in range(spare_mandates):
            # Find sum of mandates of both lists
            jointmandates = mandates.dot(self.surplus_matrix)

            # Find the cost (voters per mandates) of each set of parties
            jointcost = jointvoters/(jointmandates+1)

            # Find the parties with maximal voters to mandates ratio
            idx = np.nonzero(self.surplus_matrix[:,np.argmax(jointcost)])[0]

            # Find the ratio of each party in the set
            individual_cost = threshold_sample[idx]/(mandates[idx] + 1)

            # Award winning party an extra mandate
            mandates[idx[np.argmax(individual_cost)]] += 1

        return mandates
