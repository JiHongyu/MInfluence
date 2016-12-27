import collections
import numpy as np

class SpreadMethod:

    @classmethod
    def determin_spread(cls, g, target, sources):
        pass

    @classmethod
    def determin_influence(cls, g, u, v):
        pass

class LTMethod(SpreadMethod):

    @classmethod
    def determin_spread(cls, g, target, sources):

        sum_influ = sum((g.edge[s][target]['ltm_infl'] for s in sources))
        if sum_influ > g.node[target]['ltm_thrd']:
            return True
        else:
            return False

    @classmethod
    def determin_influence(cls, g, u, v=None):
        if g.node[u]['status']:
            return True
        else:
            return False

class ICMethod(SpreadMethod):

    icm_status = collections.defaultdict(bool)

    @classmethod
    def determin_spread(cls, g, target, sources):
        rands = np.random.random(len(sources))
        for s, r in zip(sources, rands):
            if g.edge[s][target]['icm_prob'] > r:
                return True
        return False

    @classmethod
    def determin_influence(cls, g, u, v):
        if g.node[u]['status'] and not cls.icm_status[u, v]:
            cls.icm_status[u, v] = True
            return True
        else:
            return False

class Diffusion_Simulation:
    def __init__(self, network, spread_method, prec_neighbors=None):
        self.network = network
        self.spread_method = spread_method

        # 前驱邻居，在有向网络中非常重要的索引
        if prec_neighbors is None:
            self.prec_neighbors = collections.defaultdict(list)
            for u in network.nodes_iter():
                for v in network.neighbors_iter(u):
                    self.prec_neighbors[v].append(u)
        else:
            self.prec_neighbors = prec_neighbors


    def clear_status(self):

        for v in self.network.nodes_iter():
            self.network.node[v]['status'] = False
        pass

    def simulation(self, seed_vertices, seed_type, iter_maximum):

        g = self.network

        # 种子节点初始状态
        for v in seed_vertices:
            g.node[v]['status'] = True

        # 初始化激活节点和静默节点集合
        active_vertices = set(seed_vertices)
        silence_vertices = set(g.nodes()) - active_vertices

        for iter_n in range(iter_maximum):

            # 一次迭代计算

            cur_iter_active = []
            for sv in silence_vertices:

                sv_type = g.node[sv]['category']

                # 可能激活该节点的前驱邻居节点
                prec_infl_neigs_cate = collections.defaultdict(list)
                for x in self.prec_neighbors[sv]:
                    x_type = g.node[x]['category']
                    mc = self.spread_method[x_type, sv_type]
                    if mc.determin_influence(g, x, sv):
                        prec_infl_neigs_cate[g.node[x]['category']].append(x)

                # 依次用不同类型的方式尝试激活该节点 sv，只要激活就 OKey
                for t in prec_infl_neigs_cate:

                    mc = self.spread_method[t, sv_type]
                    if mc.determin_spread(g, sv, prec_infl_neigs_cate[t]):
                        cur_iter_active.append(sv)
                        break

            # 更新一次迭代后的激活节点信息

            if len(cur_iter_active) is 0:
                break

            for cur_a_v in cur_iter_active:
                g.node[cur_a_v]['status'] = True

            active_vertices.update(cur_iter_active)
            silence_vertices.difference_update(cur_iter_active)

        # 统计目标集合节点被激活数目
        target_actived_num = 0
        for v in g.nodes_iter():
            if g.node[v]['category'] == seed_type and v in active_vertices:
                target_actived_num += 1

        return target_actived_num











