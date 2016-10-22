class BipartideSolver(object):
    __slots__ = ['E', 'V', 'C', 'F', 'visited', 'total_flow']

    def __init__(self, E):
        # edges
        self.E = E

        # vertices
        self.V = set([])
        for u, v, c in E:
            self.V.add(u)
            self.V.add(v)

        # flow
        self.F = {}

        # capacity
        self.C = {(u, v): c for u, v, c in E}

        self.visited = set([])
        self.total_flow = None

    def send(self, u, v, minn):
        '''
        Sends at most minn flow between nodes u and v.
        Peforms a DFS to find a path connecting them.
        '''
        self.visited.add(u)

        if u == v:
            return minn

        for t in self.V:
            if t in self.visited:
                continue

            C_edge = self.C.get((u, t), 0) - self.F.get((u, t), 0)

            if C_edge:
                sent = self.send(t, v, min(minn, C_edge))
                if sent:
                    self.F[(u, t)] = self.F.get((u, t), 0) + sent
                    self.F[(t, u)] = self.F.get((t, u), 0) - sent
                    return sent
        return 0

    def solve(self):
        self.total_flow = 0
        source = min(self.V)
        sink = max(self.V)

        while True:
            sent = self.send(source, sink, float('inf'))
            if sent:
                self.total_flow += sent
            else:
                break
            self.visited.clear()
        return self.total_flow

    def print_flow(self):
        print('total flow: %i' % self.total_flow)
        for (u, v), c in self.F.items():
            if c > 0:
                print('%i -> %i : %i' % (u, v, c))
