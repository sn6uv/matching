#!/usr/bin/env python

"""
Ford-Fulkerson pattern matcher.

"""

__author__ = "Angus Griffith"
__copyright__ = "Copyright 2016, Angus Griffith"
__status__ = "Prototype"


import logging


logging.basicConfig(level=logging.INFO)


def matchQ(patt, arg):
    # TODO placeholder
    return patt == arg


def print_c(C):
    return ', '.join(sorted('%i -> %i' % uv for uv, c in C.items() if c > 0))


class Matcher(object):
    def __init__(self, patts, args):
        self.k = len(patts)
        self.m = len(args)
        self.source = 0
        self.sink = self.k + self.m + 1
        self.V = list(range(self.k + self.m + 2))      # vertices

        self.F = {}     # flow
        self.C = {}     # capacity
        self.init(patts, args)

        self.visited = set([])
        self.total_flow = None
        logging.debug(print_c(self.C))

    def init(self, patts, args):
        # patts to args
        capacity = set([])
        for i, patt in enumerate(patts):
            for j, arg in enumerate(args):
                if matchQ(patt, arg):
                    capacity.add((i + 1, j + self.k + 1))
        for i in self.V:
            for j in self.V:
                self.C[i, j] = 1 if (i, j) in capacity else 0
                self.F[i, j] = 0

        # source to patts
        for i, patt in enumerate(patts):
            self.C[self.source, i + 1] = 1

        # args to sink
        for j, arg in enumerate(args):
            self.C[j + self.k + 1, self.sink] = 1

    def match(self, construct=False):
        logging.debug('Binding patterns.')
        bound_patts = self.bind_patts()
        logging.info('Bound %i/%i patterns.' % (bound_patts, self.k))
        if bound_patts < self.k:
            if construct:
                return None
            else:
                return False

        logging.debug('Binding arguments.')
        bound_args = self.bind_args()
        logging.info('Bound %i/%i arguments.' % (bound_args, self.m))
        if bound_args < self.m:
            if construct:
                return None
            else:
                return False

        logging.debug('Constructing match.')
        if construct:
            return self.construct_match()
        else:
            return True

    def bind_patts(self):
        return self.bind(False)

    def bind_args(self):
        return self.bind(True)

    def bind(self, is_args):
        total = 0

        while True:
            sent = self.send(self.source, self.sink, 2**63, reverse=is_args)
            if sent:
                logging.debug('sent %i flow through the graph' % (sent,))
                total += sent
            else:
                break
            self.visited.clear()

        return total

    def send(self, u, v, minn, reverse=False):
        '''
        send flow through the graph.
        performs a DFS
        '''
        logging.debug('sending %i flow %i->%i.' % (minn, u, v))
        self.visited.add(u)

        if u == v:
            return minn

        for t in self.V:
            if t in self.visited:
                continue

            C_edge = self.C[u, t] - self.F[u, t]

            if C_edge > 0:
                sent = self.send(t, v, min(minn, C_edge))
                if sent:
                    self.F[u, t] += sent
                    self.F[t, u] -= sent
                    return sent
        return 0


    def construct_match(self):
        raise NotImplementedError


m = Matcher([1, 2], [1, 2])
m.match()
