import collections

import networkx as nx
import numpy as np

import SPAlgorithm as SP
from .abc_network import ABC


class TwitterData(ABC):

    def __init__(self, path):

        self.network = nx.read_gexf(path)

        prec_neighbr = collections.defaultdict(list)
        for u in self.network.nodes_iter():
            for v in self.network.neighbors_iter(u):
                prec_neighbr[v].append(u)

        for n in self.network.nodes_iter():
            self.network.node[n]['ltm_thrd'] = np.random.random()
            self.network.node[n]['status'] = False

        for u, v in self.network.edges_iter():
            self.network.edge[u][v]['icm_prob'] = np.random.random() / 1
            self.network.edge[u][v]['ltm_infl'] = np.random.random()

        for u in self.network.nodes_iter():
            cate = collections.defaultdict(list)
            for v in prec_neighbr[u]:
                cate[self.network.node[v]['category']].append(v)
            for c in cate:
                for v in cate[c]:
                    self.network.edge[v][u]['ltm_infl'] /= len(cate[c])

        self.spread_methods = {('user', 'user'):   SP.ICMethod,
                               ('tweet', 'tweet'): SP.ICMethod,
                               ('user', 'tweet'):  SP.ICMethod,
                               ('tweet', 'user'):  SP.ICMethod}

        self.target = 'user'

    @property
    def data(self):
        return self.network, self.spread_methods, self.target
