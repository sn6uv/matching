import unittest

from flattening import Expression, flatten


class TestFlatten(unittest.TestCase):
    def testAtom(self):
        expr = Expression('f', 1)
        self.assertEqual(flatten(expr), expr)

    def testExpression(self):
        expr = Expression('f', Expression('f', 1))
        self.assertEqual(flatten(expr), Expression('f', 1))

        expr = Expression('f', 1, Expression('f', 2, 3), 4)
        self.assertEqual(flatten(expr), Expression('f', 1, 2, 3, 4))

    def testNestedExpression(self):
        expr = Expression('f', 1, Expression('g', Expression('f', 2, 3), 4), 5)
        self.assertEqual(flatten(expr), expr)

    def testEmpty(self):
        expr = Expression('f', 1, Expression('f'), 2)
        self.assertEqual(flatten(expr), Expression('f', 1, 2))

        expr = Expression('f', 1, Expression('f', Expression('f')), 2)
        self.assertEqual(flatten(expr), Expression('f', 1, 2))
