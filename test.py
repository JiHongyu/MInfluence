import collections
import pickle
import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import heter_data as Heter
# 1. 构建网络

# Vertex attributions: category, status, ltm_thrd
# Link attributions: icm_prob, ltm_infl

if os.path.exists('result/im.pickle'):
    g = pickle.load(open('result/im.pickle', 'rb'))
else:
    g = Heter.test_network()
    pickle.dump(g, open('result/im.pickle', 'wb'))
    nx.write_gexf(g, 'result/im.gexf')


# 反转网络的连接关系，但是其属性关系没变
nx.reverse(g, copy=False)

# 2. 确定传播方式
# icm, ltm
spread_methods = {('t1', 't1'): 'ltm',
                  ('t2', 't2'): 'ltm',
                  ('t1', 't2'): 'icm',
                  ('t2', 't1'): 'icm'}

def determin_spread(g, target, sources, method):

    if method is 'icm':
        rands = np.random.random(len(sources))
        for s, r in zip(sources, rands):
            if g.edge[s][target]['icm_prob'] > r:
                return True
        return False
    elif method is 'ltm':
        sum_influ = sum((g.edge[s][target]['ltm_infl'] for s in sources))
        if sum_influ > g.node[target]['ltm_thrd']:
            return True
        else:
            return False
    else:
        raise Exception("Method Error in def determin_spread()")
# 3. 设置种子节点

seed_vertices = [0, 1, 2]

# 4.模拟扩散

number_of_iteration = 50

for v in seed_vertices:
    g.node[v]['status'] = True

active_vertices = set(seed_vertices)
silence_vertices = set(g.nodes()) - active_vertices

# ICM 激活标识，每条边只能被激活一次
icm_status = collections.defaultdict(bool)

number_of_node = len(g.nodes())
res = []
for iter_n in range(number_of_iteration):

    cur_iter_active = []
    for sv in silence_vertices:

        sv_type = g.node[sv]['category']

        succ_active_neigs = []

        for x in g.neighbors_iter(sv):
            if g.node[x]['status']:
                m = spread_methods[g.node[x]['category'], sv_type]
                if m is 'ltm':
                    succ_active_neigs.append(x)
                elif m is 'icm' and not icm_status[x, sv]:
                    icm_status[x, sv] = True
                    succ_active_neigs.append(x)

        neigs_cate = collections.defaultdict(list)

        for neig in succ_active_neigs:
            neigs_cate[g.node[neig]['category']].append(neig)

        for t in neigs_cate:
            m = spread_methods[t, sv_type]
            if determin_spread(g, sv, neigs_cate[t], m):
                cur_iter_active.append(sv)
                break

    for av in cur_iter_active:
        g.node[av]['status'] = True
    active_vertices.update(cur_iter_active)
    silence_vertices.difference_update(cur_iter_active)

    res.append(len(active_vertices)/number_of_node)

nx.reverse(g, copy=False)

nx.write_gexf(g, 'result/im_algo.gexf')

plt.plot(res)
plt.show()







