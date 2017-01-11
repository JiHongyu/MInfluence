class ABC:

    def __init__(self):
        self.network = None
        self.spread_methods = None
        self.target = None

    def print_info(self):

        all_nodes_num = self.network.number_of_nodes()
        target_node_num = sum((1 for x in self.network.nodes_iter() if self.network.node[x]['category'] == self.target))

        all_edge_num = self.network.number_of_edges()

        print('------Networks info-----')
        print('总点数: %d，总边数: %d'%(all_nodes_num, all_edge_num))
        print('目标节点数: %d'%target_node_num)
        print('------------------------')