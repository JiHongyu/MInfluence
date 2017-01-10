import collections
import functools

import os
import pickle

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

import HeterData as HData
import SPAlgorithm as SP
import MIAlgorithm as MI

# 选择数据

network_data = HData.TwitterData('./result/tweet_100_without_0_outer.gexf')

g, spread_methods, target_type = network_data.data

# 种子点数 K 的选择
K = 20

# 重复模拟次数
repeat_number = 30


simulator = SP.NetworkDiffusion(g, spread_methods, prec_neighbors=None, repeat_number=repeat_number)

algorithms = collections.OrderedDict()
algorithms['degr_c'] = MI.Centrality(simulator, target_type, K, nx.degree_centrality)
# algorithms['vec_c'] = MI.Centrality(simulator, target_type, K, functools.partial(nx.eigenvector_centrality, tol=1.0e-3, weight=None))
# algorithms['greedy'] = MI.OriGreedy(simulator, target_type, K)
algorithms['celf++'] = MI.CelfPlus(simulator, target_type, K)


col_name = list(algorithms.keys())

res = collections.OrderedDict()

for name in algorithms:
    algorithms[name].run()
    res[name] = algorithms[name].influence

df = pd.DataFrame(data=res)

df.plot()
plt.show()

