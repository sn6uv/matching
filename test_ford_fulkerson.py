from ford_fulkerson import BipartideSolver

# 0 is source, n - 1 is sink
E = [
    # from source
    (0, 1, 1),
    (0, 2, 1),
    (0, 3, 1),
    # middle
    (1, 4, 1),
    (1, 5, 1),
    (2, 5, 1),
    (2, 6, 1),
    (3, 5, 1),
    (3, 6, 1),
    # to sink
    (4, 7, 1),
    (5, 7, 1),
    (6, 7, 1),
]

b = BipartideSolver(E)
b.solve()
assert b.total_flow == 3
# b.print_flow()


# 0 is source, n - 1 is sink
E = [
    # from source
    (0, 1, 1),
    (0, 2, 1),
    (0, 3, 1),
    # middle
    (1, 4, 1),
    (1, 6, 1),
    (2, 5, 1),
    (3, 4, 1),
    # to sink
    (4, 7, 1),
    (5, 7, 1),
    (6, 7, 1),
]

b = BipartideSolver(E)
b.solve()
assert b.total_flow == 3
# b.print_flow()
