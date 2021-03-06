#!/usr/bin/env python

"""
Ford-Fulkerson pattern matcher.
"""

__author__ = "Angus Griffith"
__copyright__ = "Copyright 2016, Angus Griffith"
__status__ = "Prototype"


import logging
from collections import defaultdict


def print_flow(C):
    return ', '.join(sorted('%i->%i: %i' % (u, v, c) for (u, v), c in C.items() if c > 0))


class Matcher(object):
    def __init__(self, patts, args):
        self.k = len(patts)
        self.m = len(args)
        self.source = 0
        self.sink = self.k + self.m + 1
        self.V = list(range(self.k + self.m + 2))      # vertices

        self.patt_names = {i + 1: patt.name for i, patt in enumerate(patts)}
        self.arg_values = {j + self.k + 1: arg for j, arg in enumerate(args)}

        self.F = defaultdict(int)     # flow
        self.C = defaultdict(int)     # min capacity
        self.D = defaultdict(int)     # max capacity

        self.init_edges(patts, args)

        self.visited = set([])
        self.total_flow = None
        logging.debug(print_flow(self.C))
        logging.debug(print_flow(self.D))

    def init_edges(self, patts, args):
        '''
        Construct the edges for a bipartide graph V = (L, U) where L = patts
        and R = args. Node l in L is connected to node r in R iff l matches r.
        '''

        # patts to args
        for i, patt in enumerate(patts):
            for j, arg in enumerate(args):
                if patt.matchQ(arg):
                    self.C[i + 1, j + self.k + 1] = 1
                    self.D[i + 1, j + self.k + 1] = 1

        # source to patts
        for i, patt in enumerate(patts):
            self.C[self.source, i + 1] = patt.capacity[0]
            self.D[self.source, i + 1] = patt.capacity[1]

        # args to sink
        for j, arg in enumerate(args):
            self.C[j + self.k + 1, self.sink] = 1
            self.D[j + self.k + 1, self.sink] = 1

    def match(self, construct=False):
        '''
        Pushes flow through the graph to determine a matching.
        '''
        logging.info('Binding patterns...')
        bound_patts = self.bind_patts()
        logging.debug(print_flow(self.F))
        if bound_patts:
            logging.info('Success.')
        else:
            logging.info('Failed.')
            if construct:
                return None
            else:
                return False

        logging.info('Binding arguments...')
        bound_args = self.bind_args()
        logging.debug(print_flow(self.F))
        if bound_args:
            logging.info('Success.')
        else:
            logging.info('Failed.')
            if construct:
                return None
            else:
                return False

        assert bound_patts and bound_args

        if construct:
            return self.construct_match()
        else:
            return True

    def bind_patts(self):
        '''
        Essentially Ford-Fulkerson with the first iteration of the outer loop
        interchanged with the inner loop.
        '''
        for t in self.V:
            unbound = self.C[self.source, t] - self.F[self.source, t]
            while unbound > 0:
                self.visited.add(self.source)
                sent = self.send_forwards(t, self.sink, unbound)
                self.F[self.source, t] += sent
                self.F[t, self.source] -= sent
                if sent == 0:
                    return False
                unbound -= sent
            self.visited.clear()
        return True

    def bind_args(self):
        '''
        see bind_patts
        '''
        for t in self.V:
            unbound = self.C[t, self.sink] - self.F[t, self.sink]
            while unbound > 0:
                self.visited.add(self.sink)
                sent = self.send_backwards(self.source, t, unbound)
                self.F[t, self.sink] += sent
                self.F[self.sink, t] -= sent
                if sent == 0:
                    return False
                unbound -= sent
            self.visited.clear()
        return True

    def send_forwards(self, u, v, minn):
        '''
        send flow through the graph.
        performs a DFS to find the next step.
        recurses towards the sink (forwards).
        '''

        self.visited.add(u)

        if u == v:
            return minn

        for t in self.V:
            if t in self.visited:
                continue
            C_edge = self.C[u, t] - self.F[u, t]
            if C_edge > 0:
                sent = self.send_forwards(t, v, min(minn, C_edge))
                if sent:
                    self.F[u, t] += sent
                    self.F[t, u] -= sent
                    return sent
        return 0

    def send_backwards(self, u, v, minn):
        '''
        see send_forwards.
        recurses towards the source (backwards).
        '''

        self.visited.add(v)

        if u == v:
            return minn

        for t in self.V:
            if t in self.visited:
                continue
            C_edge = self.D[t, v] - self.F[t, v]
            if C_edge > 0:
                sent = self.send_backwards(u, t, min(minn, C_edge))
                if sent:
                    self.F[t, v] += sent
                    self.F[v, t] -= sent
                    return sent
        return 0

    def construct_match(self):
        '''
        given a solved flow graph returns a list of assignments
        '''
        result = defaultdict(list)
        for u in self.V:
            for v in self.V:
                if self.F[u, v] > 0 and self.F[self.source, u] > 0 and self.F[v, self.sink] > 0:
                    assert self.F[u, v] == 1
                    result[self.patt_names[u]].append(self.arg_values[v])
        result = {key: value[0] if len(value) == 1 else value for key, value in result.items()}
        return result
