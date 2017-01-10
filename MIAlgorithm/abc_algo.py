
class ABC:
    def __init__(self, simulator, target_type, K):
        self.simulator = simulator
        self.network = simulator.network
        self.target_type = target_type
        self.K = K

        self.target_nodes = tuple((x for x in self.network.node if self.network.node[x]['category'] == target_type))

        # 激活节点集合
        self.a_vertices = set()
        self.a_vertices_order = []

        #备选节点集合
        self.c_vertices = set(self.target_nodes)

        # 影响力函数信息
        self.influence = None

    def run(self):
        pass