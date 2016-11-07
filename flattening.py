"""
Flat matching
"""


class Expression(object):
    def __init__(self, head, *leaves):
        self.head = head
        self.leaves = leaves

    def __eq__(self, other):
        if isinstance(other, Expression) and self.head == other.head:
            if len(self.leaves) == len(other.leaves):
                return all(a == b for a, b in zip(self.leaves, other.leaves))
        return False

    def __str__(self):
        return '%s[%s]' % (self.head, ', '.join(str(l) for l in self.leaves))

    def __repr__(self):
        return str(self)


def _flatten(expr, head):
    if isinstance(expr, Expression) and expr.head == head:
        for leaf in expr.leaves:
            for sub_expr in _flatten(leaf, head):
                yield sub_expr
    else:
        yield expr


def flatten(expr):
    """
    fully flattens an expression
    """
    head = expr.head
    new_leaves = _flatten(expr, head)
    return Expression(head, *new_leaves)
