import collections
import functools

import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

import HeterData as HData
import SPAlgorithm as SP
import MIAlgorithm as MI

# 选择数据

# network_data = HData.TestData(False)
network_data = HData.TwitterData('./result/tweet_100_without_0_outer.gexf')
network_data.print_info()

g, spread_methods, target_type = network_data.data

# 种子点数 K 的选择
K = 100

# 重复模拟次数
repeat_number = 400


simulator = SP.NetworkDiffusion(g, spread_methods, prec_neighbors=None, repeat_number=repeat_number)

algorithms = collections.OrderedDict()
algorithms['degr_c'] = MI.Centrality(simulator, target_type, K, nx.degree_centrality)
# algorithms['vec_c'] = MI.Centrality(simulator, target_type, K, functools.partial(nx.eigenvector_centrality, tol=1.0e-3, weight=None))
algorithms['greedy'] = MI.OriGreedy(simulator, target_type, K)
algorithms['celf++'] = MI.CelfPlus(simulator, target_type, K)

mi_res = collections.OrderedDict()
time_res = collections.OrderedDict()

pre_time = time.time()
for name in algorithms:
    algorithms[name].run()
    cur_time = time.time()

    mi_res[name] = algorithms[name].influence
    time_res[name] = cur_time - pre_time
    pre_time = cur_time


plt.style.use('ggplot')

df = pd.DataFrame(data=mi_res)
df.plot(grid=True)
plt.show()

if 'greedy' in algorithms:
    simi_res = collections.OrderedDict()
    greedy_a = algorithms['greedy'].a_vertices_order
    for name in algorithms:
        if name == 'greedy':
            continue
        a = algorithms[name].a_vertices_order

        g_a_s = set()
        a_s = set()
        _t = []
        for x, y in zip(greedy_a, a):
            g_a_s.add(x)
            a_s.add(y)
            simi = len(g_a_s.intersection(a_s))/len(g_a_s.union(a_s))
            _t.append(simi)

        simi_res[name] = _t

    simi_df = pd.DataFrame(data=simi_res)
    simi_df.plot(grid=True)
    plt.show()


