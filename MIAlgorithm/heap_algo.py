from .abc_algo import ABC

import pandas as pd
import heapq


class HeapUnit:

    def __init__(self, v):
        self.v = v
        self.mg = 0
        self.influence = 0
        self.flag = 0

    def __gt__(self, other):
        if self.mg < other.mg:
            return True


class HeapAlgo(ABC):

    def __init__(self, simulator, target_type, K):
        ABC.__init__(self, simulator, target_type, K)

    def run(self):

        print('HeapAlgo Algorithm')

        info = []
        # initial
        hp = []

        for v in self.target_nodes:

            unit = HeapUnit(v)
            d = self.simulator.simulation({v}, self.target_type)
            unit.mg = d['target_a_n']
            unit.influence = d['target_a_n']
            heapq.heappush(hp, unit)

        # simulation
        cnt = 0
        while len(self.a_vertices) < self.K:

            unit = heapq.heappop(hp)

            if len(self.a_vertices) == unit.flag:
                print('%d' % cnt)
                cnt += 1

                self.a_vertices.add(unit.v)
                self.a_vertices_order.append(unit.v)
                info.append(unit.influence)
                continue
            else:
                unit.mg, unit.influence = self.simulator.marginal_gain(
                    self.a_vertices, unit.v, self.target_type)
                unit.flag = len(self.a_vertices)
                heapq.heappush(hp, unit)

        self.influence = info




