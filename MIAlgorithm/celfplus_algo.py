from .abc_algo import ABC

import pandas as pd
import heapq

class SCELF:

    def __init__(self, v):
        self.v = v
        self.mg1 = 0
        self.g1 = 0
        self.prev_best = None
        self.mg2 = 0
        self.g2 = 0
        self.flag = 0

    def __gt__(self, other):
        if self.mg1 < other.mg1:
            return True

class CelfPlus(ABC):

    def __init__(self, simulator, target_type, K):
        ABC.__init__(self, simulator, target_type, K)

    def run(self):

        print('CELF++ Algorithm')

        info = []
        # initial
        hp = []
        last_seed = None
        cur_best = None

        for v in self.target_nodes:

            celf = SCELF(v)
            d = self.simulator.simulation({v}, self.target_type)
            celf.mg1 = d['target_a_n']

            if cur_best is None:
                celf.prev_best = v
                celf.mg2 = celf.mg1
            else:
                celf.prev_best = cur_best
                d = self.simulator.simulation({v, cur_best}, self.target_type)
                celf.mg2 = d['target_a_n']

            heapq.heappush(hp, celf)
            cur_best = hp[0].v

        # simulation

        cnt = 0
        while len(self.a_vertices) < self.K:

            celf = heapq.heappop(hp)

            if len(self.a_vertices) == celf.flag:
                print('%d' % cnt)
                cnt += 1

                self.a_vertices.add(celf.v)
                self.a_vertices_order.append(celf.v)
                last_seed = celf.v
                info.append(celf.g1)
                continue
            elif celf.prev_best == last_seed:
                celf.mg1, celf.g1 = celf.mg2, celf.g2
            else:
                celf.mg1, celf.g1 = self.simulator.marginal_gain(self.a_vertices, celf.v, self.target_type)
                celf.prev_best = cur_best
                celf.mg2, celf.g2 = self.simulator.marginal_gain(self.a_vertices.union({cur_best}), celf.v, self.target_type)

            celf.flag = len(self.a_vertices)
            heapq.heappush(hp, celf)
            cur_best = hp[0].v

        self.influence = info




