
import itertools
import collections

import networkx as nx
import numpy as np

def test_network():
    g = nx.DiGraph()

    g1 = nx.powerlaw_cluster_graph(n=100, m=3, p=0.3)

    # g1 = nx.scale_free_graph(n=100)

    num_of_node = g1.number_of_nodes()

    nodes_1 = [x for x in g1.nodes()]
    for n in g1.nodes():
        g.add_node(n,
                   category='t1', status=False, ltm_thrd=np.random.rand())
    for n1, n2 in g1.edges_iter():
        g.add_edge(n2, n1,
                   icm_prob=np.random.rand(), ltm_infl=np.random.random())

    g2 = nx.fast_gnp_random_graph(n=30, p=0.3, directed=True)

    nodes_2 = [x+num_of_node for x in g2.nodes()]

    for n in g2.nodes():
        g.add_node(n+num_of_node,
                   category='t2', status=False, ltm_thrd=np.random.random())

    for n1, n2 in g2.edges_iter():
        g.add_edge(n1+num_of_node, n2+num_of_node,
                   icm_prob=np.random.rand(), ltm_infl=np.random.random())

    for n1, n2 in itertools.product(nodes_1, nodes_2):
        if np.random.rand() < 0.1:
            g.add_edge(n1, n2,
                       icm_prob=np.random.random(),
                       ltm_infl=np.random.random())
        if np.random.rand() < 0.1:
            g.add_edge(n2, n1,
                       icm_prob=np.random.random(),
                       ltm_infl=np.random.random())

    prec_neigs_cate = collections.defaultdict(list)

    for u in g.nodes_iter():
        for v in g.neighbors_iter(u):
            prec_neigs_cate[v].append(u)

    for u in g.nodes_iter():
        cate = collections.defaultdict(list)
        for v in prec_neigs_cate[u]:
            cate[g.node[v]['category']].append(v)
        for c in cate:
            for v in cate[c]:
                g.edge[v][u]['ltm_infl'] = g.edge[v][u]['ltm_infl'] / len(cate[c])

    return g
