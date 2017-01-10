from .abc_algo import ABC

import pandas as pd

class OriGreedy(ABC):

    def __init__(self, simulator, target_type, K):
        ABC.__init__(self, simulator, target_type, K)

    def run(self):
        print('Oringal Greedy Algorithm')
        info = []
        for iter_n in range(self.K):

            print('-------%2d--------' % iter_n)

            max_d = {'target_a_n': -1}
            max_v = None

            for v in self.c_vertices:
                d = self.simulator.simulation(self.a_vertices.union({v}), self.target_type)
                if max_d['target_a_n'] < d['target_a_n']:
                    max_d = d
                    max_v = v

            self.a_vertices.add(max_v)
            self.a_vertices_order.append(max_v)
            self.c_vertices.remove(max_v)
            info.append(max_d['target_a_n'])

        self.influence = info

