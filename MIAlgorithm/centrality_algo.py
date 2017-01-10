from .abc_algo import ABC

class Centrality(ABC):

    def __init__(self, simulator, target_type, K, central_func):
        ABC.__init__(self, simulator, target_type, K)
        self.central_func = central_func

    def run(self):

        print('Centrality Algorithm')
        info = []

        _t = self.central_func(self.network)

        central = []

        for n in self.target_nodes:
            central.append((n, _t[n]))

        central.sort(key=lambda x: x[1], reverse=True)

        cnt = 0
        for v, c in central:

            cnt += 1

            if cnt > self.K:
                break

            self.a_vertices.add(v)
            self.a_vertices_order.append(v)

            d = self.simulator.simulation(self.a_vertices, self.target_type)

            info.append(d['target_a_n'])

        self.influence = info



