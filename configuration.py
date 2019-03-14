
import json
import numpy as np

class Configuration:
    def __init__(self, json_path):
        with open(json_path) as json_file:
            commentless_content = '\n'.join(map(lambda x: x[:x.find('//')], json_file.readlines()))
            conf = json.loads(commentless_content)
            self._conf = conf

        self.num_mandates = conf["NUM_MANDATES"]
        self.threshold = conf["AHUZ_HAHASIMA"]
        self.num_voters = conf["NUM_LEGAL_VOTERS"]
        self.constant_drift = conf["CONSTANT_DRIFT"]
        self.relative_drift = conf["RELATIVE_DRIFT"]
        self.candidates_support = conf["CANDIDATES"]
        self.i_to_key = dict()
        for i, key in enumerate(self.candidates_support.keys()):
            self.i_to_key[i] = key
        self.key_to_i = {v: k for k, v in self.i_to_key.items()}
        self.surplus_agreement = conf["SURPLUS_AGREEMENT"]

        # This matrix contains a row for each party participating in the elections,
        # and a column for each set of parites  in a surplus agreement.
        # Whenever a party is part of a surplus agreement, there is a '1'. othrewise, '0'.
        self.surplus_matrix = np.zeros((len(self.candidates_support)-1, len(self.surplus_agreement)), dtype=np.int16)
        for i, participants in enumerate(self.surplus_agreement):
            for participant in participants:
                self.surplus_matrix[self.key_to_i[participant], i] = 1
