import unittest

from ordered_matcher import Matcher
from patterns import BlankPattern, RawPattern, BlankSequencePattern, BlankNullSequencePattern


def matchQ(patts, args):
    m = Matcher(patts, args)
    return m.match()



class MatchTest(unittest.TestCase):
    def _get_matching(self, patts, args):
        m = Matcher(patts, args)
        self.assertTrue(m.match())
        return dict(m.matches)

    def assertMatchEqual(self, patts, args, result):
        self.assertEqual(self._get_matching(patts, args), result)

    def assertMatchTrue(self, patts, args):
        self.assertTrue(matchQ(patts, args))

    def assertMatchFalse(self, patts, args):
        self.assertFalse(matchQ(patts, args))

    def test_blank(self):
        self.assertMatchTrue([BlankPattern('x')], [1])
        self.assertMatchTrue([BlankPattern('x'), BlankPattern('y')], [1, 2])
        self.assertMatchEqual([BlankPattern('x')], [1], {'x': [1]})
        self.assertMatchEqual([BlankPattern('x'), BlankPattern('y')], [1, 2], {'x': [1], 'y': [2]})

    def test_blank_none(self):
        self.assertMatchFalse([BlankPattern('x')], [])

    def test_blank_too_many(self):
        self.assertMatchFalse([BlankPattern('x')], [1, 2])
        self.assertMatchFalse([BlankPattern('x'), BlankPattern('y')], [1, 2, 3])

    def test_blanksequence(self):
        self.assertMatchTrue([BlankSequencePattern('x')], [1])
        self.assertMatchTrue([BlankSequencePattern('x')], [1, 2])
        self.assertMatchTrue([BlankSequencePattern('x')], [1, 2, 3])
        self.assertMatchEqual([BlankSequencePattern('x')], [1, 2, 3], {'x': [1, 2, 3]})

    def test_blanksequence_none(self):
        self.assertMatchFalse([BlankSequencePattern('x')], [])

    def test_blanksequence_multi(self):
        self.assertMatchFalse([BlankSequencePattern('x'), BlankSequencePattern('y')], [])
        self.assertMatchFalse([BlankSequencePattern('x'), BlankSequencePattern('y')], [1])
        self.assertMatchTrue([BlankSequencePattern('x'), BlankSequencePattern('y')], [1, 2])
        self.assertMatchTrue([BlankSequencePattern('x'), BlankSequencePattern('y')], [1, 2, 3])
        self.assertMatchTrue([BlankSequencePattern('x'), BlankSequencePattern('y')], [1, 2, 3, 4, 5])
        self.assertMatchEqual([BlankSequencePattern('x'), BlankSequencePattern('y')], [1, 2, 3], {'x': [1], 'y': [2, 3]})

    def test_blanknullsequence(self):
        self.assertMatchTrue([BlankNullSequencePattern('x')], [])
        self.assertMatchTrue([BlankNullSequencePattern('x')], [1])
        self.assertMatchTrue([BlankNullSequencePattern('x')], [1, 2])
        self.assertMatchEqual([BlankNullSequencePattern('x')], [], {'x': []})
        self.assertMatchEqual([BlankNullSequencePattern('x')], [1], {'x': [1]})
        self.assertMatchEqual([BlankNullSequencePattern('x')], [1, 2], {'x': [1, 2]})

    def test_blanknullsequence_multi(self):
        self.assertMatchTrue([BlankNullSequencePattern('x'), BlankNullSequencePattern('y')], [])
        self.assertMatchEqual([BlankNullSequencePattern('x'), BlankNullSequencePattern('y')], [], {'x': [], 'y': []})
        self.assertMatchEqual([BlankNullSequencePattern('x'), BlankNullSequencePattern('y')], [1], {'x': [], 'y': [1]})
        self.assertMatchEqual([BlankNullSequencePattern('x'), BlankNullSequencePattern('y')], [1, 2], {'x': [], 'y': [1, 2]})

    def test_raw(self):
        self.assertMatchTrue([RawPattern('x', 1)], [1])

    def test_raw_blank(self):
        self.assertMatchFalse([BlankPattern('x'), BlankPattern('y'), RawPattern('z', 1)], [1, 2, 3])
        self.assertMatchTrue([BlankPattern('x'), BlankPattern('y'), RawPattern('z', 1)], [3, 2, 1])

    def test_push(self):
        self.assertMatchEqual(
            [BlankSequencePattern('x'), RawPattern('y', 1), BlankSequencePattern('z')],
            [3, 2, 1, 4, 5],
            {'x': [3, 2], 'y': [1], 'z': [4, 5]})
