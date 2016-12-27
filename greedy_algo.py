import pickle
import os

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

import heter_data as Heter

import Spread as SP



def compute_centrality(g, central_func, nodes):

    _t = central_func(g)

    central = []

    for n in nodes:
        central.append((n, _t[n]))

    central.sort(key=lambda x: x[1], reverse=True)


    return [x for x,y in central]


# 1. 构建网络

# Vertex attributions: category, status, ltm_thrd
# Link attributions: icm_prob, ltm_infl

if os.path.exists('result/im.pickle'):
    g = pickle.load(open('result/im.pickle', 'rb'))
else:
    g = Heter.test_network()
    pickle.dump(g, open('result/im.pickle', 'wb'))
    nx.write_gexf(g, 'result/im.gexf')



# 2. 确定传播方式
# icm, ltm
spread_methods = {('t1', 't1'): SP.LTMethod,
                  ('t2', 't2'): SP.LTMethod,
                  ('t1', 't2'): SP.ICMethod,
                  ('t2', 't1'): SP.ICMethod}

simulator = SP.Diffusion_Simulation(g, spread_methods)

K = 30
repeat_number = 5
A = set()
target_type = 't1'

target_nodes = tuple((x for x in g.node if g.node[x]['category'] == target_type))

# 计算中心性

degree_centrality = compute_centrality(g, nx.degree_centrality, target_nodes)
eigenvector_centrality = compute_centrality(g, nx.eigenvector_centrality, target_nodes)

a_vertices = set()
c_vertices = set(target_nodes)
res = []
for iter_n in range(K):

    max_gain = -100
    max_v = None

    print('-------%2d--------' % iter_n)

    for v in c_vertices:
        g_a_v = 0
        g_a = 0
        for r in range(repeat_number):
            simulator.clear_status()
            g_a_v += simulator.simulation(a_vertices.union({v}), target_type, 30)
            #g_a += simulator.simulation(a_vertices, target_type, 50)

        if g_a_v > max_gain:
            max_gain = g_a_v
            max_v = v

    a_vertices.add(max_v)
    c_vertices.remove(max_v)
    dc = 0
    ec = 0
    for r in range(repeat_number):
        simulator.clear_status()
        dc += simulator.simulation(degree_centrality[0:iter_n+1], target_type, 30)
        ec += simulator.simulation(eigenvector_centrality[0:iter_n + 1], target_type, 30)
    res.append((max_gain/repeat_number, dc/repeat_number, ec/repeat_number))

df = pd.DataFrame(data=res, columns=['ga', 'degree', 'eigv'])
plt.plot(df)
plt.show()




