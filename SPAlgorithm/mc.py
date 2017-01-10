import collections
import numpy as np

class SpreadMethod:

    @classmethod
    def determin_spread(cls, g, target, source):
        pass

    @classmethod
    def determin_influence(cls, g, u, v):
        pass

class LTMethod(SpreadMethod):

    @classmethod
    def determin_spread(cls, g, target, source, prec_neighbors):

        s_type = g.node[source]['category']

        # 同类型激活邻居
        neighbors_iter = (n for n in prec_neighbors[target]
                          if g.node[n]['category'] == s_type and g.node[n]['status'])
        sum_influ = sum((g.edge[s][target]['ltm_infl'] for s in neighbors_iter))

        return True if sum_influ > g.node[target]['ltm_thrd'] else False


class ICMethod(SpreadMethod):

    @classmethod
    def determin_spread(cls, g, target, source, prec_neighbors=None):

        r = np.random.random()
        return True if g.edge[source][target]['icm_prob'] > r else False


class NetworkDiffusion:
    def __init__(self, network, spread_method, prec_neighbors=None, repeat_number=20):
        self.network = network
        self.spread_method = spread_method
        self.repeat_num = repeat_number

        # 前驱邻居，在有向网络中非常重要的索引
        if prec_neighbors is None:
            self.prec_neighbors = collections.defaultdict(list)
            for u in network.nodes_iter():
                for v in network.neighbors_iter(u):
                    self.prec_neighbors[v].append(u)
        else:
            self.prec_neighbors = prec_neighbors

    def __clear_status(self):

        for v in self.network.nodes_iter():
            self.network.node[v]['status'] = False
        pass

    def simulation(self, seed_vertices, seed_type):

        iter_maximum = self.network.number_of_nodes() - 1

        g = self.network

        target_n = 0
        for v in g.nodes_iter():
            if g.node[v]['category'] == seed_type:
                target_n += 1

        res = dict()
        res['target_a_n'] = 0
        res['other_a_n'] = 0
        res['all_a_n'] = 0
        res['target_n'] = target_n
        res['other_n'] = g.number_of_nodes() - target_n
        res['all_n'] = g.number_of_nodes()

        for x in range(self.repeat_num):
            self.__clear_status()

            # 种子节点初始状态
            for v in seed_vertices:
                g.node[v]['status'] = True

            # 初始化激活节点和静默节点集合
            active_vertices = set(seed_vertices)
            silence_vertices = set(g.nodes()) - active_vertices

            # 迭代传播时当前激活节点和前次迭代时的激活节点集
            pre_iter_actives = seed_vertices

            for iter_n in range(iter_maximum):

                # 一次迭代计算
                cur_iter_active = []
                for pa in pre_iter_actives:
                    pa_type = g.node[pa]['category']

                    # 激活节点的静默邻居
                    silence_neighbors_iter = \
                        (nei for nei in g.neighbors_iter(pa) if not g.node[nei]['status'])

                    # 对静默邻居分别进行尝试激活
                    for sv in silence_neighbors_iter:
                        sv_type = g.node[sv]['category']
                        mc = self.spread_method[pa_type, sv_type]
                        if mc.determin_spread(g, sv, pa, self.prec_neighbors):
                            cur_iter_active.append(sv)

                # 更新一次迭代后的激活节点信息

                if len(cur_iter_active) is 0:
                    break

                for cur_a_v in cur_iter_active:
                    g.node[cur_a_v]['status'] = True

                active_vertices.update(cur_iter_active)
                pre_iter_actives = cur_iter_active

            # 统计目标集合节点被激活数目
            target_actived_num = 0
            for v in g.nodes_iter():
                if g.node[v]['category'] == seed_type and v in active_vertices:
                    target_actived_num += 1

            res['target_a_n'] += target_actived_num
            res['all_a_n'] += len(active_vertices)

        res['target_a_n'] /= self.repeat_num
        res['all_a_n'] /= self.repeat_num
        res['other_a_n'] = res['all_a_n'] - res['target_a_n']

        return res

    def marginal_gain(self, seed_vertices, u, seed_type):

        d1 = self.simulation(seed_vertices.union({u}), seed_type)
        d2 = self.simulation(seed_vertices, seed_type)

        return d1['target_a_n'] - d2['target_a_n'], d1['target_a_n']


